import requests
from typing import List

class OsintService:
    @staticmethod
    def get_tech_stack(domain: str) -> List[str]:
        """
        Detects technologies using HTTP headers and HTML content.
        """
        technologies = set()
        url = f"http://{domain}"
        try:
            response = requests.get(url, timeout=5, verify=False)
            headers = response.headers
            
            # 1. Check Headers
            if 'Server' in headers:
                technologies.add(f"Server: {headers['Server']}")
            if 'X-Powered-By' in headers:
                technologies.add(f"Powered By: {headers['X-Powered-By']}")
            if 'X-AspNet-Version' in headers:
                technologies.add("ASP.NET")
            
            # 2. Check Cookies
            cookies = response.cookies.get_dict()
            if 'PHPSESSID' in cookies:
                technologies.add("PHP")
            if 'JSESSIONID' in cookies:
                technologies.add("Java/JSP")
            if 'csrftoken' in cookies: # Common in Django
                technologies.add("Django (Potential)")
                
            # 3. Simple HTML Content checks
            content = response.text.lower()
            if 'wp-content' in content:
                technologies.add("WordPress")
            if 'react' in content:
                technologies.add("React (Frontend)")
            # 4. WAF Detection
            if 'cf-ray' in headers or 'cf-cache-status' in headers:
                technologies.add("WAF: Cloudflare")
            if 'x-amz-cf-id' in headers:
                technologies.add("WAF: AWS CloudFront")
            if 'server' in headers and 'akamai' in headers['server'].lower():
                technologies.add("WAF: Akamai")
            if 'x-sucuri-id' in headers:
                technologies.add("WAF: Sucuri")

            return list(technologies)
            
        except requests.RequestException:
            return ["Unknown (Host unreachable)"]
