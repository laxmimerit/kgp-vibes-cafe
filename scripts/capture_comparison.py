"""
capture_comparison.py
Captures desktop (1280px) and phone (390px) screenshots for Home, Menu, Cart, and Checkout
from both the current site (http://localhost:8000) and Stitch reference screens.
"""
import http.server
import socketserver
import threading
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PORT = 8000
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(BASE_DIR, "site")
REF_DIR = os.path.join(BASE_DIR, "stitch_reference")
OUT_DIR = os.path.join(BASE_DIR, "comparison_screenshots")
os.makedirs(OUT_DIR, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIR, **kwargs)

    def log_message(self, format, *args):
        pass

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("", PORT), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

def set_desktop_mode(driver):
    driver.execute_cdp_cmd('Emulation.clearDeviceMetricsOverride', {})
    driver.set_window_size(1280, 900)
    time.sleep(0.5)

def set_mobile_mode(driver):
    driver.set_window_size(480, 950)
    driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
        'width': 390,
        'height': 844,
        'deviceScaleFactor': 2,
        'mobile': True
    })
    time.sleep(0.5)

def capture_screenshot(driver, filepath, is_mobile=False):
    total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
    target_height = min(total_height, 6000)
    
    if is_mobile:
        driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': target_height,
            'deviceScaleFactor': 2,
            'mobile': True
        })
    else:
        driver.set_window_size(1280, target_height)

    time.sleep(0.5)
    driver.save_screenshot(filepath)
    print(f"Captured {os.path.basename(filepath)} (target height {target_height})")

def main():
    server = start_server()
    print(f"Server started on http://localhost:{PORT}")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    try:
        # Pre-seed cart items
        driver.get(f"http://localhost:{PORT}/menu.html")
        time.sleep(1)
        driver.execute_script("""
            const sampleCart = [
                { id: "kv-coffee-01", name: "Talkie Chai", category: "Chai", price: 2.00, quantity: 2 },
                { id: "kv-pastry-01", name: "Byte Brownie", category: "Snacks", price: 2.50, quantity: 1 },
                { id: "kv-coffee-02", name: "Filter Coffee", category: "Coffee", price: 2.50, quantity: 1 }
            ];
            localStorage.setItem("kgp_cart", JSON.stringify(sampleCart));
        """)

        pages = [
            ("home", f"http://localhost:{PORT}/index.html"),
            ("menu", f"http://localhost:{PORT}/menu.html"),
            ("cart", f"http://localhost:{PORT}/cart.html"),
            ("checkout", f"http://localhost:{PORT}/checkout.html")
        ]

        print("\n--- Capturing Updated Site Pages ---")
        for name, url in pages:
            # Desktop
            set_desktop_mode(driver)
            driver.get(url)
            time.sleep(1)
            capture_screenshot(driver, os.path.join(OUT_DIR, f"after_site_{name}_desktop.png"), is_mobile=False)

            # Mobile (390px)
            set_mobile_mode(driver)
            driver.get(url)
            time.sleep(1)
            capture_screenshot(driver, os.path.join(OUT_DIR, f"after_site_{name}_mobile.png"), is_mobile=True)

        print("\n--- Capturing Stitch Reference Pages ---")
        ref_screens = [
            ("home_desktop", os.path.join(REF_DIR, "desktop_home.html"), False),
            ("home_mobile", os.path.join(REF_DIR, "mobile_home.html"), True),
            ("menu_desktop", os.path.join(REF_DIR, "desktop_menu.html"), False),
            ("menu_mobile", os.path.join(REF_DIR, "desktop_menu.html"), True),
            ("cart_desktop", os.path.join(REF_DIR, "desktop_cart.html"), False),
            ("cart_mobile", os.path.join(REF_DIR, "mobile_cart.html"), True),
            ("checkout_desktop", os.path.join(REF_DIR, "desktop_checkout.html"), False),
            ("checkout_mobile", os.path.join(REF_DIR, "mobile_checkout.html"), True),
        ]

        for name, path, is_mob in ref_screens:
            if os.path.exists(path):
                if is_mob:
                    set_mobile_mode(driver)
                else:
                    set_desktop_mode(driver)
                driver.get("file:///" + path.replace("\\", "/"))
                time.sleep(1)
                capture_screenshot(driver, os.path.join(OUT_DIR, f"exact_ref_{name}.png"), is_mobile=is_mob)

    finally:
        driver.quit()
        server.shutdown()
        server.server_close()
        print("\nAll comparison screenshots captured successfully!")

if __name__ == "__main__":
    main()
