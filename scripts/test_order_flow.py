"""
test_order_flow.py
End-to-end verification of KGP Vibes Cafe website order flow in a real headless Chrome browser,
including pickup time behavior across multiple times of day, cart quantity/total updates,
and confirmation ticket verification.
"""
import http.server
import socketserver
import threading
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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(BASE_DIR, "site")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIR, **kwargs)

    def log_message(self, format, *args):
        pass  # suppress server logs

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, BrokenPipeError):
            pass


def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("", PORT), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def safe_click(driver, el):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    time.sleep(0.1)
    el.click()


def set_simulated_time(driver, hh_mm_str):
    """Simulate a specific time of day (HH:MM in 24h) on the cart page and refresh pickup UI."""
    hours, minutes = map(int, hh_mm_str.split(":"))
    driver.execute_script(
        """
        const d = new Date();
        d.setHours(arguments[0], arguments[1], 0, 0);
        window.refreshPickupTimeOptions(d);
        """,
        hours,
        minutes,
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
    print(f"HTTP Server started at http://localhost:{PORT}")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,1600")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Test Home Page
        print("\n--- Test 1: Home Page Loading & Navigation ---")
        driver.get(f"http://localhost:{PORT}/index.html")
        assert "KGP Vibes Cafe" in driver.title, f"Unexpected title: {driver.title}"
        brand_title = driver.find_element(By.CLASS_NAME, "brand-title").text
        assert "KGP Vibes Cafe" in brand_title, "Brand title mismatch"
        print("✓ Home page loaded successfully")

        # 2. Test Menu Page & 39 items
        print("\n--- Test 2: Menu Catalog & Dynamic Items Rendering ---")
        driver.get(f"http://localhost:{PORT}/menu.html")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "menu-card")))
        cards = driver.find_elements(By.CLASS_NAME, "menu-card")
        print(f"Rendered menu items count: {len(cards)}")
        assert len(cards) == 39, f"Expected 39 items, got {len(cards)}"
        print("✓ All 39 items from baseline/menu.csv rendered successfully")

        # Test Category Filter
        coffee_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-category="Coffee"]')
        safe_click(driver, coffee_btn)
        time.sleep(0.2)
        coffee_cards = driver.find_elements(By.CLASS_NAME, "menu-card")
        assert len(coffee_cards) == 12, f"Expected 12 coffee items, got {len(coffee_cards)}"
        print("✓ Category filter works accurately")

        # Reset Category to All
        safe_click(driver, driver.find_element(By.CSS_SELECTOR, 'button[data-category="all"]'))
        time.sleep(0.2)

        # 3. Search and Add to Cart
        print("\n--- Test 3: Add Items to Cart ---")
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
        print("✓ Items added to cart and badge updated (2 items)")

        # 4. Cart Quantities & Totals Verification
        print("\n--- Test 4: Cart Quantities & Totals Stay Correct When Quantities Change ---")
        driver.get(f"http://localhost:{PORT}/cart.html")
        wait.until(EC.presence_of_element_located((By.ID, "active-cart-layout")))

        # Initial: 1x Talkie Chai ($2.00) + 1x Byte Brownie ($2.50) = $4.50, 2 items
        assert driver.find_element(By.ID, "cart-count-summary").text == "2 items"
        assert driver.find_element(By.ID, "cart-subtotal").text == "$4.50"
        assert driver.find_element(By.ID, "cart-total").text == "$4.50"

        # Increment Talkie Chai quantity to 3 (+2 clicks) -> 3x $2.00 = $6.00 + 1x $2.50 = $8.50 (4 items)
        inc_btns = driver.find_elements(By.CSS_SELECTOR, ".btn-inc")
        safe_click(driver, inc_btns[0])
        safe_click(driver, driver.find_elements(By.CSS_SELECTOR, ".btn-inc")[0])

        rows = driver.find_elements(By.CSS_SELECTOR, "#cart-items-body tr")
        assert rows[0].find_element(By.CLASS_NAME, "qty-value").text == "3"
        assert rows[0].find_element(By.CLASS_NAME, "cart-item-total").text == "$6.00"
        assert driver.find_element(By.ID, "cart-count-summary").text == "4 items"
        assert driver.find_element(By.ID, "cart-subtotal").text == "$8.50"
        assert driver.find_element(By.ID, "cart-total").text == "$8.50"
        assert driver.find_element(By.CLASS_NAME, "cart-badge").text == "4"
        print("✓ Incrementing quantity updated row total ($6.00), subtotal ($8.50), total ($8.50), and item count (4 items)")

        #Increment Byte Brownie quantity to 2 (+1 click) -> 3x $2.00 ($6.00) + 2x $2.50 ($5.00) = $11.00 (5 items)
        safe_click(driver, driver.find_elements(By.CSS_SELECTOR, ".btn-inc")[1])
        rows = driver.find_elements(By.CSS_SELECTOR, "#cart-items-body tr")
        assert rows[1].find_element(By.CLASS_NAME, "qty-value").text == "2"
        assert rows[1].find_element(By.CLASS_NAME, "cart-item-total").text == "$5.00"
        assert driver.find_element(By.ID, "cart-count-summary").text == "5 items"
        assert driver.find_element(By.ID, "cart-subtotal").text == "$11.00"
        assert driver.find_element(By.ID, "cart-total").text == "$11.00"
        print("✓ Incrementing second item updated row total ($5.00), subtotal ($11.00), total ($11.00), and item count (5 items)")

        # Decrement Talkie Chai back to 2 (-1 click) -> 2x $2.00 ($4.00) + 2x $2.50 ($5.00) = $9.00 (4 items)
        safe_click(driver, driver.find_elements(By.CSS_SELECTOR, ".btn-dec")[0])
        rows = driver.find_elements(By.CSS_SELECTOR, "#cart-items-body tr")
        assert rows[0].find_element(By.CLASS_NAME, "qty-value").text == "2"
        assert rows[0].find_element(By.CLASS_NAME, "cart-item-total").text == "$4.00"
        assert driver.find_element(By.ID, "cart-count-summary").text == "4 items"
        assert driver.find_element(By.ID, "cart-subtotal").text == "$9.00"
        assert driver.find_element(By.ID, "cart-total").text == "$9.00"
        print("✓ Decrementing quantity updated row total ($4.00), subtotal ($9.00), total ($9.00), and item count (4 items)")

        # 5. Test Pickup Time Behavior at Several Times of Day
        print("\n--- Test 5: Pickup Time Slots & Quick Buttons Across Several Times of Day ---")

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

        # Click each quick button at 12:19 AM and verify they give 8:00 AM, 8:15 AM, 8:30 AM (not all 8:30 AM!)
        expected_closed_presets = ["8:00 AM", "8:15 AM", "8:30 AM"]
        for idx, expected_val in enumerate(expected_closed_presets):
            safe_click(driver, snap["chips"][idx])
            actual_val = driver.find_element(By.ID, "pickup-time-input").get_attribute("value")
            assert actual_val == expected_val, f"At 00:19, quick button {idx+1} gave {actual_val}, expected {expected_val}"
        print("✓ [12:19 AM - Late Night] Shows closed notice, starts at 8:00 AM, quick buttons give 8:00 AM / 8:15 AM / 8:30 AM")

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
        print("✓ [6:45 AM - Early Morning] Shows closed notice, starts at 8:00 AM, quick buttons give 8:00 AM / 8:15 AM / 8:30 AM")

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
        print("✓ [8:00 AM - Opening] Closed notice hidden, starts at 8:15 AM (>=15m from now), quick buttons give 8:15 AM / 8:30 AM / 8:45 AM")

        # 5d. Mid-day non-quarter-hour (14:07 / 2:07 PM)
        # 2:07 PM + 15m = 2:22 PM -> next 15-minute slot is 2:30 PM
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
        print("✓ [2:07 PM - Mid-day] Closed notice hidden, starts at 2:30 PM, quick buttons give 2:30 PM / 2:45 PM / 3:00 PM")

        # 5e. Near closing with 2 slots left (21:10 / 9:10 PM)
        # 9:10 PM + 15m = 9:25 PM -> next 15-minute slot is 9:30 PM. Slots: 9:30 PM, 9:45 PM.
        # +45 Mins would be 10:00 PM (after closing) -> must be hidden!
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
        print("✓ [9:10 PM - Near Closing (2 slots)] Slots are 9:30 PM & 9:45 PM; +45 Mins button hidden")

        # 5f. Near closing with 1 slot left (21:25 / 9:25 PM)
        # 9:25 PM + 15m = 9:40 PM -> next 15-minute slot is 9:45 PM. Slots: 9:45 PM.
        # +30 Mins and +45 Mins would land after closing -> both must be hidden!
        set_simulated_time(driver, "21:25")
        snap = get_pickup_ui_snapshot(driver)
        assert not snap["closed_visible"], "Closed notice must be hidden at 9:25 PM"
        assert snap["options"] == ["9:45 PM"], f"Expected ['9:45 PM'], got {snap['options']}"
        assert len(snap["visible_chips"]) == 1, f"Expected 1 visible quick button at 9:25 PM, got {len(snap['visible_chips'])}"
        assert snap["chips"][0].is_displayed()
        assert not snap["chips"][1].is_displayed(), "+30 Mins button must be hidden at 9:25 PM"
        assert not snap["chips"][2].is_displayed(), "+45 Mins button must be hidden at 9:25 PM"
        assert snap["selected"] == "9:45 PM"
        print("✓ [9:25 PM - Near Closing (1 slot)] Only 9:45 PM slot offered; +30 Mins and +45 Mins buttons hidden")

        # 5g. After last pickup cutoff (21:35 / 9:35 PM) and late night (22:45 / 10:45 PM)
        set_simulated_time(driver, "21:35")
        snap = get_pickup_ui_snapshot(driver)
        assert snap["closed_visible"], "Closed notice must be visible at 9:35 PM (past last pickup cutoff)"
        assert snap["closed_text"] == "We're closed right now. Pickup starts at 8:00 AM."
        assert snap["options"][0] == "8:00 AM"
        assert snap["selected"] == "8:00 AM"
        assert len(snap["visible_chips"]) == 3
        print("✓ [9:35 PM - Past Cutoff] Shows closed notice and starts from next opening at 8:00 AM")

        set_simulated_time(driver, "22:45")
        snap = get_pickup_ui_snapshot(driver)
        assert snap["closed_visible"], "Closed notice must be visible at 10:45 PM"
        assert snap["closed_text"] == "We're closed right now. Pickup starts at 8:00 AM."
        assert snap["options"][0] == "8:00 AM"
        assert snap["selected"] == "8:00 AM"
        print("✓ [10:45 PM - Closed Night] Shows closed notice and starts from next opening at 8:00 AM")

        # 6. Checkout & Confirmation Ticket Verification (Ticket Shows Picked Time & Updated Total)
        print("\n--- Test 6: Order Confirmation Ticket Shows Exact Customer-Picked Time & Updated Total ---")
        # Simulate 2:07 PM and pick 3:15 PM from the dropdown
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

        wait.until(EC.url_contains("confirmation.html"))
        wait.until(EC.presence_of_element_located((By.ID, "ticket-number")))

        order_number = driver.find_element(By.ID, "ticket-number").text
        customer_name = driver.find_element(By.ID, "ticket-customer").text
        pickup_time = driver.find_element(By.ID, "ticket-pickup-time").text
        outlet_name = driver.find_element(By.ID, "ticket-outlet").text
        ticket_total = driver.find_element(By.ID, "ticket-total").text

        print(f"Generated Order Number: {order_number}")
        print(f"Customer Name: {customer_name}")
        print(f"Pickup Time on Ticket: {pickup_time}")
        print(f"Outlet: {outlet_name}")
        print(f"Total on Ticket: {ticket_total}")

        assert re.match(r"^KV-\d{4}$", order_number), f"Invalid order number format: {order_number}"
        assert customer_name == "Alex Developer", f"Customer name mismatch: {customer_name}"
        assert pickup_time == "3:15 PM", f"Expected ticket pickup time '3:15 PM', got '{pickup_time}'"
        assert "Koramangala" in outlet_name, f"Outlet mismatch: {outlet_name}"
        assert ticket_total == "$9.00", f"Expected updated total '$9.00', got '{ticket_total}'"
        print("✓ Order ticket shows exact picked time ('3:15 PM') and updated cart total ('$9.00')")

        # Capture screenshot
        assets_dir = os.path.join(BASE_DIR, "assets")
        os.makedirs(assets_dir, exist_ok=True)
        screenshot_path = os.path.join(assets_dir, "demo_order_confirmation.png")
        driver.save_screenshot(screenshot_path)
        print(f"✓ Saved confirmation screenshot to {screenshot_path}")

        # 7. Test Persistence on Reload
        print("\n--- Test 7: Ticket Persistence on Reload ---")
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.ID, "ticket-number")))
        assert driver.find_element(By.ID, "ticket-number").text == order_number
        assert driver.find_element(By.ID, "ticket-pickup-time").text == "3:15 PM"
        assert driver.find_element(By.ID, "ticket-total").text == "$9.00"
        print("✓ Order ticket persisted across page refresh")

        # 8. Test Empty Cart Edge Case
        print("\n--- Test 8: Empty Cart State ---")
        safe_click(driver, driver.find_element(By.ID, "btn-another-order"))
        wait.until(EC.url_contains("menu.html"))

        driver.get(f"http://localhost:{PORT}/cart.html")
        wait.until(EC.presence_of_element_located((By.ID, "empty-cart-state")))
        assert driver.find_element(By.ID, "empty-cart-state").is_displayed()
        assert not driver.find_element(By.ID, "active-cart-layout").is_displayed()
        print("✓ Empty cart state verified")

        # 9. Test Direct Confirmation Protection
        print("\n--- Test 9: Direct Visit to Confirmation without Order ---")
        driver.get(f"http://localhost:{PORT}/confirmation.html")
        wait.until(EC.url_contains("menu.html"))
        print("✓ Direct visit to confirmation.html without active order redirected to menu.html")

        print("\n=======================================================")
        print("ALL END-TO-END TESTS PASSED SUCCESSFULLY!")
        print(f"GOAL ACHIEVED: Verified across 8 times of day, Order Number: {order_number}")
        print("=======================================================\n")

    finally:
        driver.quit()
        server.shutdown()
        server.server_close()
        print("Server and browser stopped cleanly.")


if __name__ == "__main__":
    run_tests()
