from playwright.async_api import async_playwright
import os
import base64
from typing import Dict

class VisualReconService:
    @staticmethod
    async def take_screenshots(subdomains: list[str]) -> Dict[str, str]:
        """
        Takes screenshots of the given subdomains (up to 5 to save time/resources).
        Returns a dict of {subdomain: base64_image_string}.
        """
        screenshots = {}
        # Limit to first 5 subdomains for performance in this demo
        targets = subdomains[:5]
        
        async with async_playwright() as p:
            # Launch browser (headless)
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={'width': 1280, 'height': 720})
            
            for sub in targets:
                page = await context.new_page()
                try:
                    url = f"http://{sub}"
                    # Timeout after 5s
                    await page.goto(url, timeout=10000, wait_until="domcontentloaded")
                    screenshot_bytes = await page.screenshot(type='jpeg', quality=50) # Compress for storage
                    
                    # Convert to base64 for easy storage in DB/JSON
                    b64_img = base64.b64encode(screenshot_bytes).decode('utf-8')
                    screenshots[sub] = f"data:image/jpeg;base64,{b64_img}"
                    print(f"Screenshot taken for {sub}")
                    
                except Exception as e:
                    print(f"Failed to screenshot {sub}: {e}")
                finally:
                    await page.close()
            
            await browser.close()
            
        return screenshots
