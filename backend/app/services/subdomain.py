import requests
import dns.resolver
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

class SubdomainService:
    @staticmethod
    def get_subdomains_crtsh(domain: str) -> List[str]:
        """
        Query crt.sh for subdomains using Certificate Transparency logs.
        """
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        
        try:
            # Random User-Agent to avoid blocking
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code != 200:
                print(f"Error fetching from crt.sh: {response.status_code}")
                return []
                
            data = response.json()
            # Extract name_value and clean up duplicates/wildcards
            subdomains = set()
            for entry in data:
                name_value = entry.get('name_value', '')
                # Split multiline entries
                for sub in name_value.split('\n'):
                    if sub and '*' not in sub:
                         # Basic cleanup
                        subdomains.add(sub.lower())
            
            return list(subdomains)
            
        except requests.RequestException as e:
            print(f"Exception querying crt.sh: {e}")
            return []

    @staticmethod
    def resolve_domains(domains: List[str]) -> List[str]:
        """
        Verify which subdomains resolve to an IP address.
        """
        resolved = []
        resolver = dns.resolver.Resolver()
        resolver.timeout = 1
        resolver.lifetime = 1
        
        for sub in domains:
            try:
                # Try to resolve A record
                resolver.resolve(sub, 'A')
                resolved.append(sub)
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
                continue
            except Exception:
                continue
                
        return resolved

    @staticmethod
    def get_subdomains_bruteforce(domain: str, wordlist_path: str = "backend/wordlists/subdomains.txt") -> List[str]:
        """
        Brute-force subdomains using a wordlist and DNS resolution.
        Uses threading for speed.
        """
        found_subdomains = set()
        
        if not os.path.exists(wordlist_path):
            print(f"Wordlist not found at {wordlist_path}")
            return []

        # Read wordlist
        try:
            with open(wordlist_path, 'r') as f:
                prefixes = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading wordlist: {e}")
            return []

        resolver = dns.resolver.Resolver()
        resolver.timeout = 1
        resolver.lifetime = 1

        def check_subdomain(prefix):
            full_domain = f"{prefix}.{domain}"
            try:
                resolver.resolve(full_domain, 'A')
                return full_domain
            except:
                return None

        # Threaded execution
        print(f"Starting brute force for {domain} with {len(prefixes)} words...")
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_domain = {executor.submit(check_subdomain, prefix): prefix for prefix in prefixes}
            
            for future in as_completed(future_to_domain):
                result = future.result()
                if result:
                    found_subdomains.add(result)
        
        print(f"Brute force finished. Found {len(found_subdomains)} subdomains.")
        return list(found_subdomains)
