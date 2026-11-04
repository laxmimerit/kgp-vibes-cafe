import http.client
import subprocess
import time
import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(BASE_DIR, "site")
PORT = 8089

def verify():
    print("Starting Next.js server on port", PORT)
    node_cmd = ["node", os.path.join("node_modules", "next", "dist", "bin", "next"), "start", "-p", str(PORT)]
    proc = subprocess.Popen(node_cmd, cwd=SITE_DIR)

    try:
        # Wait for server
        for _ in range(30):
            try:
                conn = http.client.HTTPConnection("127.0.0.1", PORT, timeout=1)
                conn.request("GET", "/")
                if conn.getresponse().status == 200:
                    break
            except Exception:
                time.sleep(0.3)

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,1800")
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
        driver = webdriver.Chrome(options=options)

        try:
            print("Loading http://localhost:8089/menu ...")
            driver.get(f"http://localhost:{PORT}/menu")
            time.sleep(1)

            cards = driver.find_elements(By.CLASS_NAME, "menu-card")
            print(f"Total menu cards rendered: {len(cards)}")

            # Check known items with and without photos
            photo_dir = os.path.join(SITE_DIR, "public", "images", "menu")
            existing_photos = {os.path.splitext(f)[0] for f in os.listdir(photo_dir) if f.endswith(".jpg")}

            checked_count = 0
            placeholder_count = 0
            img_count = 0

            # Target items to specifically assert
            target_items = ["Pumpkin Spice Latte", "Masala Chai Latte", "Vibes Espresso Shot", "Talkie Chai"]
            target_results = {}

            for card in cards:
                name = card.find_element(By.CLASS_NAME, "item-name").text
                imgs = card.find_elements(By.TAG_NAME, "img")
                placeholders = card.find_elements(By.CLASS_NAME, "menu-card-placeholder")

                checked_count += 1
                if imgs:
                    img_count += 1
                if placeholders:
                    placeholder_count += 1

                if name in target_items:
                    target_results[name] = {
                        "imgs": len(imgs),
                        "placeholders": len(placeholders),
                        "placeholder_text": placeholders[0].text if placeholders else None,
                    }

            print("\nTarget Verification Results:")
            for name, res in target_results.items():
                print(f" - {name}: {res['imgs']} img tags, {res['placeholders']} placeholders (text: {res['placeholder_text']!r})")

            # Assert Pumpkin Spice Latte
            psl = target_results["Pumpkin Spice Latte"]
            assert psl["imgs"] == 0, f"Expected 0 imgs for Pumpkin Spice Latte, got {psl['imgs']}"
            assert psl["placeholders"] == 1, f"Expected 1 placeholder for Pumpkin Spice Latte, got {psl['placeholders']}"
            assert "Coffee" in psl["placeholder_text"], f"Expected 'Coffee' in placeholder, got {psl['placeholder_text']}"

            # Assert Masala Chai Latte
            mcl = target_results["Masala Chai Latte"]
            assert mcl["imgs"] == 0, f"Expected 0 imgs for Masala Chai Latte, got {mcl['imgs']}"
            assert mcl["placeholders"] == 1, f"Expected 1 placeholder for Masala Chai Latte, got {mcl['placeholders']}"
            assert "Coffee" in mcl["placeholder_text"], f"Expected 'Coffee' in placeholder, got {mcl['placeholder_text']}"

            # Assert Vibes Espresso Shot (has photo)
            ves = target_results["Vibes Espresso Shot"]
            assert ves["imgs"] == 1, f"Expected 1 img for Vibes Espresso Shot, got {ves['imgs']}"
            assert ves["placeholders"] == 0, f"Expected 0 placeholder for Vibes Espresso Shot, got {ves['placeholders']}"

            print(f"\nOverall stats: {img_count} cards with photos, {placeholder_count} cards with clean placeholders.")
            assert placeholder_count + img_count == len(cards), "Every card must have either a photo or a placeholder!"

            # Filter to Coffee category to verify screenshot
            coffee_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-category="Coffee"]')
            coffee_btn.click()
            time.sleep(0.5)

            screenshot_path = os.path.join(BASE_DIR, "assets", "menu_placeholders_verification.png")
            driver.save_screenshot(screenshot_path)
            print(f"✓ Saved verification screenshot to {screenshot_path}")

            # Verify no 404 errors for images in console logs
            browser_logs = driver.get_log("browser")
            img_404_errors = [entry for entry in browser_logs if "/images/menu/" in entry.get("message", "") and "404" in entry.get("message", "")]
            print(f"Image 404 errors in browser console: {len(img_404_errors)}")
            assert len(img_404_errors) == 0, f"Found unexpected 404 image requests: {img_404_errors}"

            print("\n✓ ALL PLACEHOLDER CHECKS PASSED SUCCESSFULLY!")

        finally:
            driver.quit()

    finally:
        try:
            proc.terminate()
            proc.kill()
        except Exception:
            pass

if __name__ == "__main__":
    verify()
