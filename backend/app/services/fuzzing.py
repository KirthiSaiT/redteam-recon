import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

class FuzzingService:
    @staticmethod
    def brute_force_directories(domain: str, wordlist_path: str = "backend/wordlists/dir_common.txt") -> List[str]:
        """
        Brute-force common directories and files on the target domain.
        """
        found_paths = []
        base_url = f"http://{domain}"
        
        if not os.path.exists(wordlist_path):
            return []

        try:
            with open(wordlist_path, 'r') as f:
                paths = [line.strip() for line in f if line.strip()]
        except Exception:
            return []

        def check_path(path):
            url = f"{base_url}/{path}"
            try:
                # Use stream=True to avoid downloading large files
                res = requests.get(url, timeout=3, allow_redirects=False, stream=True)
                if res.status_code in [200, 301, 302, 401, 403]:
                    return f"/{path} (Status: {res.status_code})"
            except:
                pass
            return None

        # Threaded execution
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {executor.submit(check_path, path): path for path in paths}
            
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    found_paths.append(result)
        
        return found_paths
