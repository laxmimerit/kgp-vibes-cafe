"""
test_order_flow.py
End-to-end verification of KGP Vibes Cafe Next.js website order flow in a real headless Chrome browser,
including pickup time behavior across multiple times of day, cart quantity/total updates,
and confirmation ticket verification.
"""
import http.client
import subprocess
import time
import os
import re
import sys

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

PORT = 8089
DEV_PORT = 3000
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(BASE_DIR, "site")


def is_port_open(port):
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
        conn.request("GET", "/")
        resp = conn.getresponse()
        return resp.status == 200
    except Exception:
        return False


def start_server():
    print(f"Starting Next.js production server on port {PORT}...", flush=True)
    next_entry = os.path.join("node_modules", "next", "dist", "bin", "next")
    node_cmd = ["node", next_entry, "start", "-p", str(PORT)]

    proc = subprocess.Popen(
        node_cmd,
        cwd=SITE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    start_time = time.time()
    while time.time() - start_time < 30:
        try:
            conn = http.client.HTTPConnection("127.0.0.1", PORT, timeout=1)
            conn.request("GET", "/")
            resp = conn.getresponse()
            if resp.status == 200:
                print(f"✓ Next.js server ready at http://localhost:{PORT}/", flush=True)
                return proc
        except Exception:
            time.sleep(0.3)

    try:
        proc.terminate()
        proc.kill()
    except Exception:
        pass
    raise RuntimeError(f"Next.js server failed to respond on port {PORT} within 30 seconds.")


def safe_click(driver, el):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    time.sleep(0.1)
    el.click()


def set_simulated_time(driver, hh_mm_str):
    """Simulate a specific time of day (HH:MM in 24h) on the cart page and refresh pickup UI."""
    hours, minutes = map(int, hh_mm_str.split(":"))
    driver.execute_async_script(
        """
        const [hours, minutes, done] = arguments;
        const d = new Date();
        d.setHours(hours, minutes, 0, 0);
        window.refreshPickupTimeOptions(d);
        requestAnimationFrame(() => setTimeout(done, 0));
        """,
        hours,
        minutes,
    )


def assert_no_console_errors(driver, context_label):
    """Fail if the browser logged any unexpected console.error / uncaught JS / hydration errors."""
    unexpected = []
    for entry in driver.get_log("browser"):
        if entry.get("level") != "SEVERE":
            continue
        msg = entry.get("message", "")
        # Menu page intentionally falls back via onError for items without custom photography
        if "/images/menu/" in msg and "404" in msg:
            continue
        # Ignore external Google Fonts network errors if tested without internet
        if ("fonts.googleapis.com" in msg or "fonts.gstatic.com" in msg) and "ERR_" in msg:
            continue
        unexpected.append(entry)

    assert not unexpected, (
        f"Unexpected browser console error(s) during {context_label}: {unexpected}"
    )


def get_pickup_ui_snapshot(driver):
    """Read closed notice visibility/text, dropdown options, selected value, and quick button states."""
    closed_el = driver.find_element(By.ID, "cafe-closed-notice")
    select_el = driver.find_element(By.ID, "pickup-time-input")
    select_obj = Select(select_el)
    options = [opt.text for opt in select_obj.options]
    selected = select_el.get_attribute("value")

    chips = driver.find_elements(By.CSS_SELECTOR, ".time-chip")
    visible_chips = [c for c in chips if c.is_displayed()]
    hidden_chips = [c for c in chips if not c.is_displayed()]

    return {
        "closed_visible": closed_el.is_displayed(),
        "closed_text": closed_el.text.strip() if closed_el.is_displayed() else "",
        "options": options,
        "selected": selected,
        "chips": chips,
        "visible_chips": visible_chips,
        "hidden_chips": hidden_chips,
    }


def run_tests():
    server = start_server()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,1600")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Test Home Page
        print("\n--- Test 1: Home Page Loading & Navigation ---", flush=True)
        driver.get(f"http://localhost:{PORT}/")
        assert "KGP Vibes Cafe" in driver.title, f"Unexpected title: {driver.title}"
        brand_title = driver.find_element(By.CLASS_NAME, "brand-title").text
        assert "KGP Vibes Cafe" in brand_title, "Brand title mismatch"
        print("✓ Home page loaded successfully", flush=True)

        # 2. Test Menu Page & Dynamic Items
        print("\n--- Test 2: Menu Catalog & Dynamic Items Rendering ---", flush=True)
        menu_json_path = os.path.join(SITE_DIR, "data", "menu.json")
        expected_total = 40
        expected_coffee = 13
        if os.path.exists(menu_json_path):
            import json
            with open(menu_json_path, mode="r", encoding="utf-8") as f:
                menu_data = json.load(f)
                expected_total = len(menu_data)
                expected_coffee = len([item for item in menu_data if item.get("category") == "Coffee"])

        driver.get(f"http://localhost:{PORT}/menu")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "menu-card")))
        cards = driver.find_elements(By.CLASS_NAME, "menu-card")
        print(f"Rendered menu items count: {len(cards)}", flush=True)
        assert len(cards) == expected_total, f"Expected {expected_total} items, got {len(cards)}"
        print(f"✓ All {expected_total} items from baseline/menu.csv rendered successfully", flush=True)

        # Test Category Filter
        coffee_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-category="Coffee"]')
        safe_click(driver, coffee_btn)
        time.sleep(0.2)
        coffee_cards = driver.find_elements(By.CLASS_NAME, "menu-card")
        assert len(coffee_cards) == expected_coffee, f"Expected {expected_coffee} coffee items, got {len(coffee_cards)}"
        print("✓ Category filter works accurately", flush=True)

        # Reset Category to All
        safe_click(driver, driver.find_element(By.CSS_SELECTOR, 'button[data-category="all"]'))
        time.sleep(0.2)

        # 3. Search and Add to Cart
        print("\n--- Test 3: Add Items to Cart ---", flush=True)
        search_input = driver.find_element(By.ID, "menu-search")
        search_input.send_keys("Talkie Chai")
        time.sleep(0.2)
        chai_card = driver.find_element(By.CLASS_NAME, "menu-card")
        assert "Talkie Chai" in chai_card.text
        safe_click(driver, chai_card.find_element(By.CLASS_NAME, "add-to-cart-btn"))
        time.sleep(0.3)

        # Clear search and add Byte Brownie
        search_input.clear()
        search_input.send_keys("Byte Brownie")
        time.sleep(0.2)
        brownie_card = driver.find_element(By.CLASS_NAME, "menu-card")
        assert "Byte Brownie" in brownie_card.text
        safe_click(driver, brownie_card.find_element(By.CLASS_NAME, "add-to-cart-btn"))
        time.sleep(0.3)

        badges = driver.find_elements(By.CLASS_NAME, "cart-badge")
        cart_count = int(badges[0].text)
        assert cart_count == 2, f"Expected 2 items in cart, got {cart_count}"
        print("✓ Items added to cart and badge updated (2 items)", flush=True)

        # 4. Cart Quantities & Totals Verification
        print("\n--- Test 4: Cart Quantities & Totals Stay Correct When Quantities Change ---", flush=True)
        driver.get(f"http://localhost:{PORT}/cart")
        wait.until(EC.visibility_of_element_located((By.ID, "active-cart-layout")))
        assert_no_console_errors(driver, "Cart page load & hydration")

        # Determine actual item prices from menu data
        menu_json_path = os.path.join(SITE_DIR, "data", "menu.json")
        chai_price = 2.00
        brownie_price = 2.50
        if os.path.exists(menu_json_path):
            import json
            with open(menu_json_path, mode="r", encoding="utf-8") as f:
                menu_data = json.load(f)
                for item in menu_data:
                    if item.get("name") == "Talkie Chai":
                        chai_price = float(item["price"])
                    elif item.get("name") == "Byte Brownie":
                        brownie_price = float(item["price"])

        expected_initial_subtotal = f"${(chai_price + brownie_price):.2f}"
        expected_chai_3 = f"${(chai_price * 3):.2f}"
        expected_step1_subtotal = f"${(chai_price * 3 + brownie_price):.2f}"
        expected_brownie_2 = f"${(brownie_price * 2):.2f}"
        expected_step2_subtotal = f"${(chai_price * 3 + brownie_price * 2):.2f}"
        expected_chai_2 = f"${(chai_price * 2):.2f}"
        expected_final_total = f"${(chai_price * 2 + brownie_price * 2):.2f}"

        # Initial: 1x Talkie Chai + 1x Byte Brownie
        assert driver.find_element(By.ID, "cart-count-summary").text == "2 items"
        assert driver.find_element(By.ID, "cart-subtotal").text == expected_initial_subtotal
        assert driver.find_element(By.ID, "cart-total").text == expected_initial_subtotal

        # Increment Talkie Chai quantity to 3 (+2 clicks)
        inc_btns = driver.find_elements(By.CSS_SELECTOR, ".btn-inc")
        safe_click(driver, inc_btns[0])
        safe_click(driver, driver.find_elements(By.CSS_SELECTOR, ".btn-inc")[0])

        rows = driver.find_elements(By.CSS_SELECTOR, "#cart-items-body tr")
        assert rows[0].find_element(By.CLASS_NAME, "qty-value").text == "3"
        assert rows[0].find_element(By.CLASS_NAME, "cart-item-total").text == expected_chai_3
        assert driver.find_element(By.ID, "cart-count-summary").text == "4 items"
        assert driver.find_element(By.ID, "cart-subtotal").text == expected_step1_subtotal
        assert driver.find_element(By.ID, "cart-total").text == expected_step1_subtotal
        assert driver.find_element(By.CLASS_NAME, "cart-badge").text == "4"
        print(f"✓ Incrementing quantity updated row total ({expected_chai_3}), subtotal ({expected_step1_subtotal}), total ({expected_step1_subtotal}), and item count (4 items)", flush=True)

        # Increment Byte Brownie quantity to 2 (+1 click)
        safe_click(driver, driver.find_elements(By.CSS_SELECTOR, ".btn-inc")[1])
        rows = driver.find_elements(By.CSS_SELECTOR, "#cart-items-body tr")
        assert rows[1].find_element(By.CLASS_NAME, "qty-value").text == "2"
        assert rows[1].find_element(By.CLASS_NAME, "cart-item-total").text == expected_brownie_2
        assert driver.find_element(By.ID, "cart-count-summary").text == "5 items"
        assert driver.find_element(By.ID, "cart-subtotal").text == expected_step2_subtotal
        assert driver.find_element(By.ID, "cart-total").text == expected_step2_subtotal
        print(f"✓ Incrementing second item updated row total ({expected_brownie_2}), subtotal ({expected_step2_subtotal}), total ({expected_step2_subtotal}), and item count (5 items)", flush=True)

        # Decrement Talkie Chai back to 2 (-1 click)
        safe_click(driver, driver.find_elements(By.CSS_SELECTOR, ".btn-dec")[0])
        rows = driver.find_elements(By.CSS_SELECTOR, "#cart-items-body tr")
        assert rows[0].find_element(By.CLASS_NAME, "qty-value").text == "2"
        assert rows[0].find_element(By.CLASS_NAME, "cart-item-total").text == expected_chai_2
        assert driver.find_element(By.ID, "cart-count-summary").text == "4 items"
        assert driver.find_element(By.ID, "cart-subtotal").text == expected_final_total
        assert driver.find_element(By.ID, "cart-total").text == expected_final_total
        print(f"✓ Decrementing quantity updated row total ({expected_chai_2}), subtotal ({expected_final_total}), total ({expected_final_total}), and item count (4 items)", flush=True)

        # 5. Test Pickup Time Behavior at Several Times of Day
        print("\n--- Test 5: Pickup Time Slots & Quick Buttons Across Several Times of Day ---", flush=True)
        print(f"Current URL at start of Test 5: {driver.current_url}", flush=True)

        # 5a. Late at night (00:19 / 12:19 AM)
        set_simulated_time(driver, "00:19")
        snap = get_pickup_ui_snapshot(driver)
        assert snap["closed_visible"], "Closed notice must be visible at 12:19 AM"
        assert snap["closed_text"] == "We're closed right now. Pickup starts at 8:00 AM."
        assert snap["options"][0] == "8:00 AM", f"Expected first slot 8:00 AM, got {snap['options'][0]}"
        assert snap["options"][-1] == "9:45 PM", f"Expected last slot 9:45 PM, got {snap['options'][-1]}"
        assert len(snap["options"]) == 56, f"Expected 56 15-min slots, got {len(snap['options'])}"
        assert snap["selected"] == "8:00 AM", f"Expected initial selection 8:00 AM, got {snap['selected']}"
        assert len(snap["visible_chips"]) == 3, "All 3 quick buttons should be visible when starting from 8:00 AM"

        # Click each quick button at 12:19 AM and verify they give 8:00 AM, 8:15 AM, 8:30 AM
        expected_closed_presets = ["8:00 AM", "8:15 AM", "8:30 AM"]
        for idx, expected_val in enumerate(expected_closed_presets):
            safe_click(driver, snap["chips"][idx])
            actual_val = driver.find_element(By.ID, "pickup-time-input").get_attribute("value")
            assert actual_val == expected_val, f"At 00:19, quick button {idx+1} gave {actual_val}, expected {expected_val}"
        print("✓ [12:19 AM - Late Night] Shows closed notice, starts at 8:00 AM, quick buttons give 8:00 AM / 8:15 AM / 8:30 AM", flush=True)

        # 5b. Early morning before opening (06:45 / 6:45 AM)
        set_simulated_time(driver, "06:45")
        snap = get_pickup_ui_snapshot(driver)
        assert snap["closed_visible"], "Closed notice must be visible at 6:45 AM"
        assert snap["closed_text"] == "We're closed right now. Pickup starts at 8:00 AM."
        assert snap["options"][0] == "8:00 AM"
        assert snap["selected"] == "8:00 AM"
        for idx, expected_val in enumerate(["8:00 AM", "8:15 AM", "8:30 AM"]):
            safe_click(driver, snap["chips"][idx])
            actual_val = driver.find_element(By.ID, "pickup-time-input").get_attribute("value")
            assert actual_val == expected_val
        print("✓ [6:45 AM - Early Morning] Shows closed notice, starts at 8:00 AM, quick buttons give 8:00 AM / 8:15 AM / 8:30 AM", flush=True)

        # 5c. Right at opening (08:00 / 8:00 AM)
        set_simulated_time(driver, "08:00")
        snap = get_pickup_ui_snapshot(driver)
        assert not snap["closed_visible"], "Closed notice must be hidden at 8:00 AM"
        assert snap["options"][0] == "8:15 AM", f"At 8:00 AM, first slot must be 8:15 AM, got {snap['options'][0]}"
        assert snap["options"][-1] == "9:45 PM"
        assert len(snap["options"]) == 55
        assert snap["selected"] == "8:15 AM"
        for idx, expected_val in enumerate(["8:15 AM", "8:30 AM", "8:45 AM"]):
            safe_click(driver, snap["chips"][idx])
            actual_val = driver.find_element(By.ID, "pickup-time-input").get_attribute("value")
            assert actual_val == expected_val
        print("✓ [8:00 AM - Opening] Closed notice hidden, starts at 8:15 AM (>=15m from now), quick buttons give 8:15 AM / 8:30 AM / 8:45 AM", flush=True)

        # 5d. Mid-day non-quarter-hour (14:07 / 2:07 PM)
        set_simulated_time(driver, "14:07")
        snap = get_pickup_ui_snapshot(driver)
        assert not snap["closed_visible"], "Closed notice must be hidden at 2:07 PM"
        assert snap["options"][0] == "2:30 PM", f"At 2:07 PM, first slot must be 2:30 PM, got {snap['options'][0]}"
        assert snap["selected"] == "2:30 PM"
        assert len(snap["visible_chips"]) == 3
        for idx, expected_val in enumerate(["2:30 PM", "2:45 PM", "3:00 PM"]):
            safe_click(driver, snap["chips"][idx])
            actual_val = driver.find_element(By.ID, "pickup-time-input").get_attribute("value")
            assert actual_val == expected_val
        print("✓ [2:07 PM - Mid-day] Closed notice hidden, starts at 2:30 PM, quick buttons give 2:30 PM / 2:45 PM / 3:00 PM", flush=True)

        # 5e. Near closing with 2 slots left (21:10 / 9:10 PM)
        set_simulated_time(driver, "21:10")
        snap = get_pickup_ui_snapshot(driver)
        assert not snap["closed_visible"], "Closed notice must be hidden at 9:10 PM"
        assert snap["options"] == ["9:30 PM", "9:45 PM"], f"Expected ['9:30 PM', '9:45 PM'], got {snap['options']}"
        assert len(snap["visible_chips"]) == 2, f"Expected 2 visible quick buttons at 9:10 PM, got {len(snap['visible_chips'])}"
        assert not snap["chips"][2].is_displayed(), "+45 Mins button must be hidden at 9:10 PM"
        safe_click(driver, snap["chips"][0])
        assert driver.find_element(By.ID, "pickup-time-input").get_attribute("value") == "9:30 PM"
        safe_click(driver, snap["chips"][1])
        assert driver.find_element(By.ID, "pickup-time-input").get_attribute("value") == "9:45 PM"
        print("✓ [9:10 PM - Near Closing (2 slots)] Slots are 9:30 PM & 9:45 PM; +45 Mins button hidden", flush=True)

        # 5f. Near closing with 1 slot left (21:25 / 9:25 PM)
        set_simulated_time(driver, "21:25")
        snap = get_pickup_ui_snapshot(driver)
        assert not snap["closed_visible"], "Closed notice must be hidden at 9:25 PM"
        assert snap["options"] == ["9:45 PM"], f"Expected ['9:45 PM'], got {snap['options']}"
        assert len(snap["visible_chips"]) == 1, f"Expected 1 visible quick button at 9:25 PM, got {len(snap['visible_chips'])}"
        assert snap["chips"][0].is_displayed()
        assert not snap["chips"][1].is_displayed(), "+30 Mins button must be hidden at 9:25 PM"
        assert not snap["chips"][2].is_displayed(), "+45 Mins button must be hidden at 9:25 PM"
        assert snap["selected"] == "9:45 PM"
        print("✓ [9:25 PM - Near Closing (1 slot)] Only 9:45 PM slot offered; +30 Mins and +45 Mins buttons hidden", flush=True)

        # 5g. After last pickup cutoff (21:35 / 9:35 PM) and late night (22:45 / 10:45 PM)
        set_simulated_time(driver, "21:35")
        snap = get_pickup_ui_snapshot(driver)
        assert snap["closed_visible"], "Closed notice must be visible at 9:35 PM (past last pickup cutoff)"
        assert snap["closed_text"] == "We're closed right now. Pickup starts at 8:00 AM."
        assert snap["options"][0] == "8:00 AM"
        assert snap["selected"] == "8:00 AM"
        assert len(snap["visible_chips"]) == 3
        print("✓ [9:35 PM - Past Cutoff] Shows closed notice and starts from next opening at 8:00 AM", flush=True)

        set_simulated_time(driver, "22:45")
        snap = get_pickup_ui_snapshot(driver)
        assert snap["closed_visible"], "Closed notice must be visible at 10:45 PM"
        assert snap["closed_text"] == "We're closed right now. Pickup starts at 8:00 AM."
        assert snap["options"][0] == "8:00 AM"
        assert snap["selected"] == "8:00 AM"
        print("✓ [10:45 PM - Closed Night] Shows closed notice and starts from next opening at 8:00 AM", flush=True)

        # 6. Checkout & Confirmation Ticket Verification
        print("\n--- Test 6: Order Confirmation Ticket Shows Exact Customer-Picked Time & Updated Total ---", flush=True)
        set_simulated_time(driver, "14:07")
        select_obj = Select(driver.find_element(By.ID, "pickup-time-input"))
        select_obj.select_by_visible_text("3:15 PM")
        picked_time_val = driver.find_element(By.ID, "pickup-time-input").get_attribute("value")
        assert picked_time_val == "3:15 PM"

        # Fill Customer Details
        driver.find_element(By.ID, "customer-name").send_keys("Alex Developer")
        driver.find_element(By.ID, "customer-phone").send_keys("9876543210")
        driver.find_element(By.ID, "special-notes").send_keys("Extra hot chai, please")

        # Submit Demo Order
        safe_click(driver, driver.find_element(By.ID, "btn-place-order"))

        wait.until(EC.url_contains("confirmation"))
        wait.until(EC.presence_of_element_located((By.ID, "ticket-number")))

        order_number = driver.find_element(By.ID, "ticket-number").text
        customer_name = driver.find_element(By.ID, "ticket-customer").text
        pickup_time = driver.find_element(By.ID, "ticket-pickup-time").text
        outlet_name = driver.find_element(By.ID, "ticket-outlet").text
        ticket_total = driver.find_element(By.ID, "ticket-total").text

        print(f"Generated Order Number: {order_number}", flush=True)
        print(f"Customer Name: {customer_name}", flush=True)
        print(f"Pickup Time on Ticket: {pickup_time}", flush=True)
        print(f"Outlet: {outlet_name}", flush=True)
        print(f"Total on Ticket: {ticket_total}", flush=True)

        assert re.match(r"^KV-\d{4}$", order_number), f"Invalid order number format: {order_number}"
        assert customer_name == "Alex Developer", f"Customer name mismatch: {customer_name}"
        assert pickup_time == "3:15 PM", f"Expected ticket pickup time '3:15 PM', got '{pickup_time}'"
        assert "Koramangala" in outlet_name, f"Outlet mismatch: {outlet_name}"
        assert ticket_total == expected_final_total, f"Expected updated total '{expected_final_total}', got '{ticket_total}'"
        print(f"✓ Order ticket shows exact picked time ('3:15 PM') and updated cart total ('{expected_final_total}')", flush=True)

        # Capture screenshot
        assets_dir = os.path.join(BASE_DIR, "assets")
        os.makedirs(assets_dir, exist_ok=True)
        screenshot_path = os.path.join(assets_dir, "demo_order_confirmation.png")
        driver.save_screenshot(screenshot_path)
        print(f"✓ Saved confirmation screenshot to {screenshot_path}", flush=True)

        # 7. Test Persistence on Reload
        print("\n--- Test 7: Ticket Persistence on Reload ---", flush=True)
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.ID, "ticket-number")))
        assert driver.find_element(By.ID, "ticket-number").text == order_number
        assert driver.find_element(By.ID, "ticket-pickup-time").text == "3:15 PM"
        assert driver.find_element(By.ID, "ticket-total").text == expected_final_total
        print("✓ Order ticket persisted across page refresh", flush=True)

        # 8. Test Empty Cart Edge Case
        print("\n--- Test 8: Empty Cart State ---", flush=True)
        safe_click(driver, driver.find_element(By.ID, "btn-another-order"))
        wait.until(EC.url_contains("menu"))

        driver.get(f"http://localhost:{PORT}/cart")
        wait.until(EC.visibility_of_element_located((By.ID, "empty-cart-state")))
        assert driver.find_element(By.ID, "empty-cart-state").is_displayed()
        assert not driver.find_element(By.ID, "active-cart-layout").is_displayed()
        assert_no_console_errors(driver, "Empty cart state")
        print("✓ Empty cart state verified", flush=True)

        # 9. Test Direct Confirmation Protection
        print("\n--- Test 9: Direct Visit to Confirmation without Order ---", flush=True)
        driver.get(f"http://localhost:{PORT}/confirmation")
        wait.until(EC.url_contains("menu"))
        assert_no_console_errors(driver, "Production full order flow")
        print("✓ Direct visit to confirmation without active order redirected to menu", flush=True)
        print("✓ Zero browser console errors across production order flow", flush=True)

        # 10. Verify Dev Server Cart Page (React Dev Mode Console Checks) when running
        if is_port_open(DEV_PORT):
            print(f"\n--- Test 10: Dev Server (port {DEV_PORT}) Cart Page Console Check ---", flush=True)
            driver.get(f"http://localhost:{DEV_PORT}/cart")
            wait.until(EC.visibility_of_element_located((By.ID, "empty-cart-state")))
            assert_no_console_errors(driver, "Dev server empty cart load")

            # Add an item on dev server, load /cart, reload /cart to test SSR + Dev Hydration with items
            driver.get(f"http://localhost:{DEV_PORT}/menu")
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "add-to-cart-btn")))
            safe_click(driver, driver.find_elements(By.CLASS_NAME, "add-to-cart-btn")[0])
            time.sleep(0.2)

            driver.get(f"http://localhost:{DEV_PORT}/cart")
            wait.until(EC.visibility_of_element_located((By.ID, "active-cart-layout")))
            driver.refresh()
            wait.until(EC.visibility_of_element_located((By.ID, "active-cart-layout")))

            # Exercise quantity buttons, quick preset chips, dropdown, and simulated time in React Dev Mode
            safe_click(driver, driver.find_element(By.CSS_SELECTOR, ".btn-inc"))
            safe_click(driver, driver.find_element(By.CSS_SELECTOR, ".btn-dec"))
            set_simulated_time(driver, "14:07")
            dev_chips = driver.find_elements(By.CSS_SELECTOR, ".time-chip")
            safe_click(driver, dev_chips[1])
            Select(driver.find_element(By.ID, "pickup-time-input")).select_by_visible_text("3:00 PM")
            safe_click(driver, driver.find_element(By.ID, "clear-all-btn"))
            wait.until(EC.visibility_of_element_located((By.ID, "empty-cart-state")))

            assert_no_console_errors(driver, "Dev server cart interactions & reload hydration")
            print(f"✓ Zero browser console errors on dev server http://localhost:{DEV_PORT}/cart", flush=True)

        print("\n=======================================================", flush=True)
        print("ALL END-TO-END TESTS PASSED SUCCESSFULLY!", flush=True)
        print(f"GOAL ACHIEVED: Verified across 8 times of day, Order Number: {order_number}", flush=True)
        print("=======================================================\n", flush=True)

    finally:
        driver.quit()
        if server:
            try:
                server.terminate()
                server.kill()
            except Exception:
                pass
        print("Server and browser stopped cleanly.", flush=True)


if __name__ == "__main__":
    run_tests()
