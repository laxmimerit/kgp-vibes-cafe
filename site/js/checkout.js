/**
 * checkout.js
 * Handles cart rendering, 15-minute pickup time slot generation/validation,
 * quick preset buttons, closed-hours messaging, outlet selection,
 * and demo order checkout.
 */

document.addEventListener('DOMContentLoaded', () => {
  const emptyState = document.getElementById('empty-cart-state');
  const activeState = document.getElementById('active-cart-layout');
  const cartItemsTable = document.getElementById('cart-items-body');
  const cartSubtotalEl = document.getElementById('cart-subtotal');
  const cartTotalEl = document.getElementById('cart-total');
  const cartCountSummaryEl = document.getElementById('cart-count-summary');
  const checkoutForm = document.getElementById('checkout-form');
  const timeAlert = document.getElementById('time-alert');
  const closedNotice = document.getElementById('cafe-closed-notice');
  const pickupTimeInput = document.getElementById('pickup-time-input');
  const presetChips = Array.from(document.querySelectorAll('.time-chip'));

  if (!activeState) return;

  // Cafe pickup schedule constants (in minutes from midnight)
  const OPEN_MINUTES = 8 * 60;          // 8:00 AM (480)
  const CLOSE_MINUTES = 21 * 60 + 45;   // 9:45 PM (1305) - last pickup slot
  const CAFE_CLOSE_MINUTES = 22 * 60;   // 10:00 PM (1320) - cafe closing time
  const SLOT_STEP = 15;                 // 15-minute slots
  const MIN_LEAD_MINUTES = 15;          // At least 15 minutes from now

  // Return current Date (supports window.__KGP_MOCK_NOW__ for testing different times of day)
  function getCurrentTime() {
    if (window.__KGP_MOCK_NOW__ !== undefined && window.__KGP_MOCK_NOW__ !== null) {
      return new Date(window.__KGP_MOCK_NOW__);
    }
    return new Date();
  }

  // Format minutes from midnight into "h:mm AM/PM" (e.g., 480 -> "8:00 AM", 1305 -> "9:45 PM")
  function formatMinutes12h(totalMinutes) {
    const hours24 = Math.floor(totalMinutes / 60);
    const mins = totalMinutes % 60;
    const period = hours24 >= 12 ? 'PM' : 'AM';
    const hours12 = hours24 % 12 === 0 ? 12 : hours24 % 12;
    const minsStr = String(mins).padStart(2, '0');
    return `${hours12}:${minsStr} ${period}`;
  }

  // Parse "h:mm AM/PM" or "HH:mm" into minutes from midnight
  function parseTimeMinutes(val) {
    if (!val || typeof val !== 'string') return null;
    const trimmed = val.trim();

    const match12 = trimmed.match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/i);
    if (match12) {
      let hours = parseInt(match12[1], 10);
      const mins = parseInt(match12[2], 10);
      const period = match12[3].toUpperCase();
      if (hours < 1 || hours > 12 || mins < 0 || mins > 59) return null;
      if (period === 'AM') {
        if (hours === 12) hours = 0;
      } else {
        if (hours !== 12) hours += 12;
      }
      return hours * 60 + mins;
    }

    const match24 = trimmed.match(/^(\d{1,2}):(\d{2})$/);
    if (match24) {
      const hours = parseInt(match24[1], 10);
      const mins = parseInt(match24[2], 10);
      if (hours < 0 || hours > 23 || mins < 0 || mins > 59) return null;
      return hours * 60 + mins;
    }

    return null;
  }

  // Compute pickup schedule state for a given Date
  function getPickupScheduleState(nowDate) {
    const now = nowDate || getCurrentTime();
    const currentMinutes = now.getHours() * 60 + now.getMinutes();
    const earliestTodaySlot = Math.ceil((currentMinutes + MIN_LEAD_MINUTES) / SLOT_STEP) * SLOT_STEP;

    let isClosed = false;
    let closedMessage = '';
    let startSlot = earliestTodaySlot;

    const nextOpeningTime = formatMinutes12h(OPEN_MINUTES);

    if (currentMinutes < OPEN_MINUTES) {
      isClosed = true;
      closedMessage = `We're closed right now. Pickup starts at ${nextOpeningTime}.`;
      startSlot = OPEN_MINUTES;
    } else if (earliestTodaySlot > CLOSE_MINUTES) {
      isClosed = true;
      closedMessage = `We're closed right now. Pickup starts at ${nextOpeningTime}.`;
      startSlot = OPEN_MINUTES;
    }

    const slots = [];
    for (let m = startSlot; m <= CLOSE_MINUTES; m += SLOT_STEP) {
      slots.push({
        minutes: m,
        label: formatMinutes12h(m)
      });
    }

    return {
      currentMinutes,
      isClosed,
      closedMessage,
      startSlot,
      slots
    };
  }

  // Sync quick button active highlight with currently selected dropdown value
  function syncActiveChipWithSelection() {
    if (!pickupTimeInput) return;
    const selectedVal = pickupTimeInput.value;
    presetChips.forEach(chip => {
      if (!chip.hidden && chip.dataset.slotValue === selectedVal) {
        chip.classList.add('active');
      } else {
        chip.classList.remove('active');
      }
    });
  }

  // Populate 15-minute pickup slots, closed notice, and quick buttons for the given time
  function refreshPickupTimeOptions(customNow) {
    if (customNow !== undefined) {
      window.__KGP_MOCK_NOW__ = customNow;
    }
    const state = getPickupScheduleState(getCurrentTime());

    // Update closed notice visibility & text
    if (closedNotice) {
      if (state.isClosed) {
        closedNotice.textContent = state.closedMessage;
        closedNotice.style.display = 'block';
      } else {
        closedNotice.style.display = 'none';
      }
    }

    // Populate <select> with valid 15-minute slots
    if (pickupTimeInput) {
      pickupTimeInput.innerHTML = '';
      state.slots.forEach(slot => {
        const opt = document.createElement('option');
        opt.value = slot.label;
        opt.textContent = slot.label;
        opt.dataset.minutes = String(slot.minutes);
        pickupTimeInput.appendChild(opt);
      });
    }

    // Configure quick buttons (+15 Mins, +30 Mins, +45 Mins) -> first 3 valid slots
    // Hide any quick button that would land after closing (9:45 PM)
    presetChips.forEach((chip, index) => {
      const targetSlot = state.slots[index];
      if (targetSlot && targetSlot.minutes <= CLOSE_MINUTES) {
        chip.style.display = '';
        chip.hidden = false;
        chip.dataset.slotValue = targetSlot.label;
        chip.dataset.slotMinutes = String(targetSlot.minutes);
      } else {
        chip.style.display = 'none';
        chip.hidden = true;
        chip.classList.remove('active');
        delete chip.dataset.slotValue;
        delete chip.dataset.slotMinutes;
      }
    });

    // Default to the first available slot (next opening time when closed, or earliest +15m slot when open)
    if (pickupTimeInput && state.slots.length > 0) {
      pickupTimeInput.value = state.slots[0].label;
    }

    syncActiveChipWithSelection();
    if (timeAlert) timeAlert.style.display = 'none';

    return state;
  }

  // Expose helper for testing different times of day
  window.refreshPickupTimeOptions = refreshPickupTimeOptions;
  window.getPickupScheduleState = getPickupScheduleState;

  // Render the current cart view and keep totals accurate
  function renderCart() {
    const cart = Cart.getCart();
    const count = Cart.getCartCount();
    const total = Cart.getCartTotal();

    if (cartSubtotalEl) cartSubtotalEl.textContent = Cart.formatPrice(total);
    if (cartTotalEl) cartTotalEl.textContent = Cart.formatPrice(total);
    if (cartCountSummaryEl) cartCountSummaryEl.textContent = `${count} ${count === 1 ? 'item' : 'items'}`;
    const totalCountBadge = document.getElementById('total-count-badge');
    if (totalCountBadge) totalCountBadge.textContent = `${count} ${count === 1 ? 'item' : 'items'}`;

    if (count === 0) {
      if (cartItemsTable) cartItemsTable.innerHTML = '';
      if (emptyState) emptyState.style.display = 'block';
      if (activeState) activeState.style.display = 'none';
      return;
    }

    if (emptyState) emptyState.style.display = 'none';
    if (activeState) activeState.style.display = 'grid';

    // Populate cart items
    if (cartItemsTable) {
      cartItemsTable.innerHTML = '';
      cart.forEach(item => {
        const tr = document.createElement('tr');
        tr.className = 'border-b border-outline-variant/15 hover:bg-surface-container-low/50 transition-colors';
        const unitPrice = Number(item.price) || 0;
        const qty = Number(item.quantity) || 0;
        const itemTotal = Math.round(unitPrice * qty * 100) / 100;
        tr.innerHTML = `
          <td class="py-space-sm pr-2">
            <div class="cart-item-info">
              <span class="cart-item-name font-headline-sm text-sm text-on-surface font-semibold block leading-tight">${item.name}</span>
              <span class="cart-item-unit font-code-pill text-xs text-primary">${Cart.formatPrice(unitPrice)} each</span>
            </div>
          </td>
          <td class="py-space-sm text-center px-1">
            <div class="card-qty-control inline-flex items-center gap-1 bg-surface-container px-2 py-1 rounded-full border border-outline-variant/30">
              <button type="button" class="qty-btn btn-dec w-6 h-6 rounded-full bg-surface-container-lowest hover:bg-surface-container-high flex items-center justify-center text-xs font-bold font-code-pill transition-colors" data-id="${item.id}" aria-label="Decrease quantity">−</button>
              <span class="qty-value font-code-pill text-xs font-semibold px-1.5">${qty}</span>
              <button type="button" class="qty-btn btn-inc w-6 h-6 rounded-full bg-surface-container-lowest hover:bg-surface-container-high flex items-center justify-center text-xs font-bold font-code-pill transition-colors" data-id="${item.id}" aria-label="Increase quantity">+</button>
            </div>
          </td>
          <td class="cart-item-total py-space-sm text-right font-headline-sm text-sm font-bold text-on-surface px-1">
            ${Cart.formatPrice(itemTotal)}
          </td>
          <td class="py-space-sm text-right pl-2">
            <button type="button" class="btn-remove text-outline hover:text-error text-xs font-bold transition-colors p-1" data-id="${item.id}" aria-label="Remove item">✕</button>
          </td>
        `;
        cartItemsTable.appendChild(tr);
      });
    }
  }

  // Handle quantity changes and removal
  if (cartItemsTable) {
    cartItemsTable.addEventListener('click', (e) => {
      const btn = e.target.closest('button');
      if (!btn) return;

      const itemId = btn.dataset.id;
      if (!itemId) return;

      if (btn.classList.contains('btn-inc')) {
        Cart.updateQuantity(itemId, 1);
        renderCart();
      } else if (btn.classList.contains('btn-dec')) {
        Cart.updateQuantity(itemId, -1);
        renderCart();
      } else if (btn.classList.contains('btn-remove')) {
        Cart.removeFromCart(itemId);
        renderCart();
      }
    });
  }

  const clearAllBtn = document.getElementById('clear-all-btn');
  if (clearAllBtn) {
    clearAllBtn.addEventListener('click', () => {
      Cart.saveCart([]);
      renderCart();
    });
  }

  // Wire quick preset buttons
  presetChips.forEach((chip, index) => {
    chip.addEventListener('click', () => {
      if (chip.hidden) return;
      const state = getPickupScheduleState(getCurrentTime());
      const targetSlot = state.slots[index];
      if (!targetSlot) return;

      if (pickupTimeInput) {
        pickupTimeInput.value = targetSlot.label;
      }
      syncActiveChipWithSelection();
      validatePickupTime();
    });
  });

  // Validate selected pickup time
  function validatePickupTime() {
    if (!pickupTimeInput || !pickupTimeInput.value) {
      showTimeError("Please select a pickup time.");
      return false;
    }

    const totalMinutes = parseTimeMinutes(pickupTimeInput.value);
    if (totalMinutes === null) {
      showTimeError("Please select a valid pickup time.");
      return false;
    }

    if (totalMinutes < OPEN_MINUTES || totalMinutes > CLOSE_MINUTES) {
      showTimeError("Pickup time must be between 8:00 AM and 9:45 PM.");
      return false;
    }

    if (totalMinutes % SLOT_STEP !== 0) {
      showTimeError("Please choose one of our 15-minute pickup slots.");
      return false;
    }

    const state = getPickupScheduleState(getCurrentTime());
    if (!state.isClosed && totalMinutes < state.startSlot) {
      showTimeError("Pickup time must be at least 15 minutes from now.");
      return false;
    }

    if (timeAlert) timeAlert.style.display = 'none';
    return true;
  }

  function showTimeError(msg) {
    if (timeAlert) {
      timeAlert.textContent = msg;
      timeAlert.style.display = 'block';
    }
  }

  if (pickupTimeInput) {
    pickupTimeInput.addEventListener('change', () => {
      syncActiveChipWithSelection();
      validatePickupTime();
    });
  }

  // Radio cards UI selection styling
  const outletRadios = document.querySelectorAll('input[name="outlet"]');
  outletRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      document.querySelectorAll('.radio-card').forEach(card => card.classList.remove('selected'));
      radio.closest('.radio-card').classList.add('selected');
    });
  });

  // Handle Demo Checkout Form Submit
  if (checkoutForm) {
    checkoutForm.addEventListener('submit', (e) => {
      e.preventDefault();

      // Ensure cart is not empty
      const cart = Cart.getCart();
      if (!cart || cart.length === 0) {
        alert("Your cart is empty.");
        return;
      }

      // Validate Customer Name (Required, min 2 chars)
      const nameInput = document.getElementById('customer-name');
      const customerName = nameInput ? nameInput.value.trim() : '';
      if (!customerName || customerName.length < 2) {
        if (nameInput) {
          nameInput.focus();
          nameInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        showTimeError("Please enter your name.");
        return;
      }

      // Validate Pickup Time
      if (!validatePickupTime()) {
        if (pickupTimeInput) {
          pickupTimeInput.focus();
          pickupTimeInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return;
      }

      // Collect Outlet Info
      const selectedOutletRadio = document.querySelector('input[name="outlet"]:checked');
      const outletVal = selectedOutletRadio ? selectedOutletRadio.value : 'koramangala';

      let outletName = "KGP Vibes Cafe - Koramangala";
      let outletAddress = "No. 27, 6th Cross, Koramangala 5th Block, Bengaluru 560095";

      if (outletVal === 'indiranagar') {
        outletName = "KGP Vibes Cafe - Indiranagar";
        outletAddress = "100 Feet Road, Indiranagar, Bengaluru 560038";
      }

      const phoneInput = document.getElementById('customer-phone');
      const customerPhone = phoneInput ? phoneInput.value.trim() : '';

      const notesInput = document.getElementById('special-notes');
      const specialNotes = notesInput ? notesInput.value.trim() : '';

      // Generate Order Ticket Number: KV- + 4-digit number
      const randomTicketNum = Math.floor(1000 + Math.random() * 9000);
      const orderNumber = `KV-${randomTicketNum}`;

      // Format chosen pickup time consistently as 12-hour slot label
      const pickedMinutes = parseTimeMinutes(pickupTimeInput.value);
      const pickedTimeLabel = pickedMinutes !== null
        ? formatMinutes12h(pickedMinutes)
        : pickupTimeInput.value;

      // Build Order Object
      const order = {
        orderNumber: orderNumber,
        customerName: customerName,
        customerPhone: customerPhone || "Not provided",
        specialNotes: specialNotes || "None",
        outletName: outletName,
        outletAddress: outletAddress,
        pickupTime: pickedTimeLabel,
        items: cart,
        total: Cart.formatPrice(Cart.getCartTotal()),
        placedAt: getCurrentTime().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      // Store in localStorage for confirmation screen
      localStorage.setItem('kgp_active_order', JSON.stringify(order));

      // Clear the cart
      Cart.clearCart();

      // Redirect to confirmation screen
      window.location.href = 'confirmation.html';
    });
  }

  // Initial setup
  refreshPickupTimeOptions();
  renderCart();
});
