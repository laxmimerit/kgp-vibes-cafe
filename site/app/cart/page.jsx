'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Cart from '../../lib/cart';

const OPEN_MINUTES = 8 * 60;          // 8:00 AM (480)
const CLOSE_MINUTES = 21 * 60 + 45;   // 9:45 PM (1305) - last pickup slot
const CAFE_CLOSE_MINUTES = 22 * 60;   // 10:00 PM (1320)
const SLOT_STEP = 15;                 // 15-minute slots
const MIN_LEAD_MINUTES = 15;          // At least 15 minutes from now

function getCurrentTime() {
  if (typeof window !== 'undefined' && window.__KGP_MOCK_NOW__ !== undefined && window.__KGP_MOCK_NOW__ !== null) {
    return new Date(window.__KGP_MOCK_NOW__);
  }
  return new Date();
}

function formatMinutes12h(totalMinutes) {
  const hours24 = Math.floor(totalMinutes / 60);
  const mins = totalMinutes % 60;
  const period = hours24 >= 12 ? 'PM' : 'AM';
  const hours12 = hours24 % 12 === 0 ? 12 : hours24 % 12;
  const minsStr = String(mins).padStart(2, '0');
  return `${hours12}:${minsStr} ${period}`;
}

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

function computePickupScheduleState(nowDate) {
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

const INITIAL_SCHEDULE_STATE = {
  currentMinutes: OPEN_MINUTES,
  isClosed: false,
  closedMessage: '',
  startSlot: OPEN_MINUTES,
  slots: [],
};

export default function CartPage() {
  const router = useRouter();
  const [hydrated, setHydrated] = useState(false);
  const [cart, setCart] = useState([]);
  const [scheduleState, setScheduleState] = useState(INITIAL_SCHEDULE_STATE);
  const [selectedTime, setSelectedTime] = useState('');
  const [selectedOutlet, setSelectedOutlet] = useState('koramangala');
  const [customerName, setCustomerName] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [specialNotes, setSpecialNotes] = useState('');
  const [timeError, setTimeError] = useState('');

  const pickupInputRef = useRef(null);

  const refreshPickupTimeOptions = useCallback((customNow) => {
    if (customNow !== undefined) {
      window.__KGP_MOCK_NOW__ = customNow;
    }
    const state = computePickupScheduleState(customNow || getCurrentTime());
    const defaultVal = state.slots.length > 0 ? state.slots[0].label : '';
    setScheduleState(state);
    setSelectedTime(defaultVal);
    setTimeError('');
    return state;
  }, []);

  useEffect(() => {
    const syncCart = () => {
      setCart(Cart.getCart());
    };

    window.refreshPickupTimeOptions = refreshPickupTimeOptions;
    window.getPickupScheduleState = computePickupScheduleState;

    syncCart();
    refreshPickupTimeOptions();
    setHydrated(true);

    window.addEventListener('kgp_cart_updated', syncCart);
    window.addEventListener('storage', syncCart);
    return () => {
      window.removeEventListener('kgp_cart_updated', syncCart);
      window.removeEventListener('storage', syncCart);
    };
  }, [refreshPickupTimeOptions]);

  const cartCount = cart.reduce((sum, item) => sum + (Number(item.quantity) || 0), 0);
  const cartTotal =
    Math.round(
      cart.reduce((sum, item) => sum + (Number(item.price) || 0) * (Number(item.quantity) || 0), 0) * 100
    ) / 100;

  const handleInc = (id) => {
    Cart.updateQuantity(id, 1);
  };

  const handleDec = (id) => {
    Cart.updateQuantity(id, -1);
  };

  const handleRemove = (id) => {
    Cart.removeFromCart(id);
  };

  const handleClearAll = () => {
    Cart.saveCart([]);
  };

  const handlePresetClick = (slot) => {
    if (!slot) return;
    setSelectedTime(slot.label);
    validatePickupTime(slot.label);
  };

  const validatePickupTime = (timeVal) => {
    const val = timeVal || selectedTime;
    if (!val) {
      setTimeError('Please select a pickup time.');
      return false;
    }
    const totalMinutes = parseTimeMinutes(val);
    if (totalMinutes === null) {
      setTimeError('Please select a valid pickup time.');
      return false;
    }
    if (totalMinutes < OPEN_MINUTES || totalMinutes > CLOSE_MINUTES) {
      setTimeError('Pickup time must be between 8:00 AM and 9:45 PM.');
      return false;
    }
    if (totalMinutes % SLOT_STEP !== 0) {
      setTimeError('Please choose one of our 15-minute pickup slots.');
      return false;
    }
    const state = computePickupScheduleState(getCurrentTime());
    if (!state.isClosed && totalMinutes < state.startSlot) {
      setTimeError('Pickup time must be at least 15 minutes from now.');
      return false;
    }
    setTimeError('');
    return true;
  };

  const handleSubmitOrder = (e) => {
    e.preventDefault();

    if (!cart || cart.length === 0) {
      alert('Your cart is empty.');
      return;
    }

    if (!customerName || customerName.trim().length < 2) {
      setTimeError('Please enter your name.');
      const el = document.getElementById('customer-name');
      if (el) el.focus();
      return;
    }

    if (!validatePickupTime(selectedTime)) {
      if (pickupInputRef.current) pickupInputRef.current.focus();
      return;
    }

    let outletName = 'KGP Vibes Cafe - Koramangala';
    let outletAddress = 'No. 27, 6th Cross, Koramangala 5th Block, Bengaluru 560095';
    if (selectedOutlet === 'indiranagar') {
      outletName = 'KGP Vibes Cafe - Indiranagar';
      outletAddress = '100 Feet Road, Indiranagar, Bengaluru 560038';
    }

    const randomTicketNum = Math.floor(1000 + Math.random() * 9000);
    const orderNumber = `KV-${randomTicketNum}`;

    const pickedMinutes = parseTimeMinutes(selectedTime);
    const pickedTimeLabel = pickedMinutes !== null ? formatMinutes12h(pickedMinutes) : selectedTime;

    const order = {
      orderNumber,
      customerName: customerName.trim(),
      customerPhone: customerPhone.trim() || 'Not provided',
      specialNotes: specialNotes.trim() || 'None',
      outletName,
      outletAddress,
      pickupTime: pickedTimeLabel,
      items: cart,
      total: Cart.formatPrice(cartTotal),
      placedAt: getCurrentTime().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    localStorage.setItem('kgp_active_order', JSON.stringify(order));
    Cart.clearCart();
    router.push('/confirmation');
  };

  return (
    <div className="w-full bg-background py-space-xl">
      <div className="max-w-[1280px] mx-auto px-gutter-desktop">
        {/* Page Title */}
        <div className="mb-space-lg">
          <h1 className="font-headline-lg text-headline-lg text-on-surface">Review Your Order &amp; Checkout</h1>
          <p className="font-body-md text-on-surface-variant mt-1">
            Review your items, choose an outlet and pickup time, and place your order ahead.
          </p>
        </div>

        {/* Empty Cart State */}
        <div
          id="empty-cart-state"
          className="bg-surface-container-lowest rounded-xl shadow-sm p-space-xl text-center flex flex-col items-center justify-center gap-space-md border border-outline-variant/30"
          style={{ display: hydrated && cartCount === 0 ? 'flex' : 'none' }}
        >
          <div className="w-20 h-20 rounded-full bg-surface-container flex items-center justify-center text-primary text-4xl">
            ☕
          </div>
          <h2 className="font-headline-md text-headline-md text-on-surface">Your cart is empty</h2>
          <p className="font-body-md text-body-md text-on-surface-variant max-w-md">
            Add your favorite brews, bites, or sweet treats from our menu to schedule a pickup.
          </p>
          <Link
            href="/menu"
            className="bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md px-space-lg py-space-sm rounded-full shadow-sm transition-all duration-200 inline-flex items-center gap-space-xs"
          >
            Browse the Menu
          </Link>
        </div>

        {/* Active Cart Layout */}
        <div
          id="active-cart-layout"
          className="grid-cols-1 lg:grid-cols-12 gap-space-lg lg:gap-gutter-desktop items-start"
          style={{ display: hydrated && cartCount > 0 ? 'grid' : 'none' }}
        >
          {/* Left: Cart Items List */}
          <div className="lg:col-span-7 flex flex-col gap-space-lg min-w-0">
            <div className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md lg:p-space-lg flex flex-col gap-space-md border border-outline-variant/30">
              <div className="flex items-center justify-between pb-space-sm border-b border-outline-variant/20">
                <div className="flex items-center gap-space-xs">
                  <span className="font-headline-sm text-headline-sm text-on-surface">Your Selected Items</span>
                  <span
                    id="total-count-badge"
                    className="font-code-pill text-xs bg-secondary-container text-on-secondary-container px-space-sm py-0.5 rounded-full font-medium"
                  >
                    {cartCount} {cartCount === 1 ? 'item' : 'items'}
                  </span>
                </div>
                <button
                  id="clear-all-btn"
                  type="button"
                  onClick={handleClearAll}
                  className="font-label-sm text-xs text-secondary hover:text-error transition-colors flex items-center gap-1 cursor-pointer"
                >
                  <span className="material-symbols-outlined text-sm">delete</span>
                  Clear Cart
                </button>
              </div>

              {/* Cart Table */}
              <table className="cart-table w-full">
                <tbody id="cart-items-body">
                  {cart.map((item) => {
                    const unitPrice = Number(item.price) || 0;
                    const qty = Number(item.quantity) || 0;
                    const itemTotal = Math.round(unitPrice * qty * 100) / 100;

                    return (
                      <tr
                        key={item.id}
                        className="border-b border-outline-variant/15 hover:bg-surface-container-low/50 transition-colors"
                      >
                        <td className="py-space-sm pr-2">
                          <div className="cart-item-info">
                            <span className="cart-item-name font-headline-sm text-sm text-on-surface font-semibold block leading-tight">
                              {item.name}
                            </span>
                            <span className="cart-item-unit font-code-pill text-xs text-primary">
                              {Cart.formatPrice(unitPrice)} each
                            </span>
                          </div>
                        </td>
                        <td className="py-space-sm text-center px-1">
                          <div className="card-qty-control inline-flex items-center gap-1 bg-surface-container px-2 py-1 rounded-full border border-outline-variant/30">
                            <button
                              type="button"
                              className="qty-btn btn-dec w-6 h-6 rounded-full bg-surface-container-lowest hover:bg-surface-container-high flex items-center justify-center text-xs font-bold font-code-pill transition-colors cursor-pointer"
                              data-id={item.id}
                              aria-label="Decrease quantity"
                              onClick={() => handleDec(item.id)}
                            >
                              −
                            </button>
                            <span className="qty-value font-code-pill text-xs font-semibold px-1.5">{qty}</span>
                            <button
                              type="button"
                              className="qty-btn btn-inc w-6 h-6 rounded-full bg-surface-container-lowest hover:bg-surface-container-high flex items-center justify-center text-xs font-bold font-code-pill transition-colors cursor-pointer"
                              data-id={item.id}
                              aria-label="Increase quantity"
                              onClick={() => handleInc(item.id)}
                            >
                              +
                            </button>
                          </div>
                        </td>
                        <td className="cart-item-total py-space-sm text-right font-headline-sm text-sm font-bold text-on-surface px-1">
                          {Cart.formatPrice(itemTotal)}
                        </td>
                        <td className="py-space-sm text-right pl-2">
                          <button
                            type="button"
                            className="btn-remove text-outline hover:text-error text-xs font-bold transition-colors p-1 cursor-pointer"
                            data-id={item.id}
                            aria-label="Remove item"
                            onClick={() => handleRemove(item.id)}
                          >
                            ✕
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>

              <div className="pt-space-sm flex justify-between items-center text-sm border-t border-outline-variant/20">
                <Link href="/menu" className="font-label-md text-primary hover:underline flex items-center gap-1 font-semibold">
                  <span className="material-symbols-outlined text-sm">add_circle</span>
                  + Add more items from menu
                </Link>
              </div>
            </div>
          </div>

          {/* Right: Pickup Details & Customer Form */}
          <div className="lg:col-span-5 flex flex-col gap-space-lg">
            <div className="bg-surface-container-lowest rounded-xl shadow-md p-space-lg flex flex-col gap-space-md border border-outline-variant/30">
              <h2 className="font-headline-sm text-headline-sm text-on-surface pb-space-xs border-b border-outline-variant/20">
                Customer Details
              </h2>

              <form id="checkout-form" onSubmit={handleSubmitOrder} className="flex flex-col gap-space-md">
                {/* 1. Outlet Selection */}
                <div className="flex flex-col gap-space-xs">
                  <label className="font-label-md text-sm text-on-surface font-semibold">
                    1. Choose Pickup Outlet
                  </label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-space-sm mt-1">
                    <label
                      className={`radio-card relative flex flex-col p-space-sm rounded-xl cursor-pointer transition-all border ${
                        selectedOutlet === 'koramangala'
                          ? 'selected bg-secondary-container text-on-secondary-container border-primary/30'
                          : 'bg-surface-container-low text-on-surface-variant hover:bg-surface-container border-outline-variant/20'
                      }`}
                    >
                      <input
                        type="radio"
                        name="outlet"
                        value="koramangala"
                        checked={selectedOutlet === 'koramangala'}
                        onChange={() => setSelectedOutlet('koramangala')}
                        className="sr-only"
                      />
                      <span className="font-label-md text-sm font-bold flex items-center justify-between">
                        Koramangala
                        {selectedOutlet === 'koramangala' && (
                          <span className="material-symbols-outlined text-primary text-base">check_circle</span>
                        )}
                      </span>
                      <span className="font-body-sm text-[11px] opacity-90 mt-0.5">
                        Open Daily · 8:00 AM – 10:00 PM
                      </span>
                    </label>

                    <label
                      className={`radio-card relative flex flex-col p-space-sm rounded-xl cursor-pointer transition-all border ${
                        selectedOutlet === 'indiranagar'
                          ? 'selected bg-secondary-container text-on-secondary-container border-primary/30'
                          : 'bg-surface-container-low text-on-surface-variant hover:bg-surface-container border-outline-variant/20'
                      }`}
                    >
                      <input
                        type="radio"
                        name="outlet"
                        value="indiranagar"
                        checked={selectedOutlet === 'indiranagar'}
                        onChange={() => setSelectedOutlet('indiranagar')}
                        className="sr-only"
                      />
                      <span className="font-label-md text-sm font-semibold flex items-center justify-between">
                        Indiranagar
                        <span className="text-[10px] bg-tertiary-fixed text-on-tertiary-fixed px-1.5 py-0.5 rounded-full font-bold">
                          Opening Soon
                        </span>
                      </span>
                      <span className="font-body-sm text-[11px] opacity-80 mt-0.5">100 Feet Road</span>
                    </label>
                  </div>
                </div>

                {/* 2. Pickup Time Selection */}
                <div className="flex flex-col gap-space-xs">
                  <label className="font-label-md text-sm text-on-surface font-semibold" htmlFor="pickup-time-input">
                    2. Choose Pickup Time
                  </label>
                  <p className="font-body-sm text-xs text-on-surface-variant">
                    Pickup times are in 15-minute slots from 8:00 AM to 9:45 PM.
                  </p>

                  <div
                    id="cafe-closed-notice"
                    className="closed-notice bg-error-container text-on-error-container p-space-sm rounded-lg font-body-sm text-sm"
                    style={{ display: scheduleState.isClosed ? 'block' : 'none' }}
                    role="status"
                  >
                    {scheduleState.closedMessage}
                  </div>

                  {/* Quick Presets (+15 Mins, +30 Mins, +45 Mins) */}
                  <div className="flex gap-space-xs mt-1" id="preset-chips-container">
                    {[0, 1, 2].map((idx) => {
                      const slot = scheduleState.slots[idx];
                      const isVisible = !!(slot && slot.minutes <= CLOSE_MINUTES);
                      const isSelected = isVisible && selectedTime === slot.label;
                      const labels = ['+15 Mins', '+30 Mins', '+45 Mins'];

                      return (
                        <button
                          key={idx}
                          type="button"
                          className={`time-chip ${isSelected ? 'active' : ''}`}
                          data-slot-value={isVisible ? slot.label : undefined}
                          data-slot-minutes={isVisible ? String(slot.minutes) : undefined}
                          style={{ display: isVisible ? 'inline-flex' : 'none' }}
                          onClick={() => isVisible && handlePresetClick(slot)}
                        >
                          {labels[idx]}
                        </button>
                      );
                    })}
                  </div>

                  <div className="mt-2 max-w-[240px]">
                    <select
                      id="pickup-time-input"
                      ref={pickupInputRef}
                      value={selectedTime}
                      onChange={(e) => {
                        const val = e.target.value;
                        setSelectedTime(val);
                        validatePickupTime(val);
                      }}
                      className="form-select w-full bg-surface-container-lowest border border-outline-variant/50 rounded-lg px-3 py-2 font-body-md text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary"
                      aria-label="Selected pickup time"
                    >
                      {scheduleState.slots.map((s) => (
                        <option key={s.minutes} value={s.label} data-minutes={String(s.minutes)}>
                          {s.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div
                    id="time-alert"
                    className="alert-box bg-error-container text-on-error-container p-2 rounded-lg text-xs mt-1"
                    style={{ display: timeError ? 'block' : 'none' }}
                  >
                    {timeError || 'Please select a valid future pickup time.'}
                  </div>
                </div>

                {/* 3. Customer Contact Fields */}
                <div className="flex flex-col gap-space-xs pt-space-xs border-t border-outline-variant/20">
                  <span className="font-label-md text-sm text-on-surface font-semibold">
                    3. Your Contact Information
                  </span>

                  <div>
                    <label className="font-label-sm text-xs text-on-surface-variant" htmlFor="customer-name">
                      Your Name <span className="text-error">*</span>
                    </label>
                    <input
                      type="text"
                      id="customer-name"
                      value={customerName}
                      onChange={(e) => setCustomerName(e.target.value)}
                      className="form-input w-full bg-surface-container-lowest border border-outline-variant/50 rounded-lg px-3 py-2 text-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary mt-0.5"
                      placeholder="e.g. Alex Developer"
                      required
                      minLength={2}
                    />
                    <span className="font-body-sm text-[11px] text-outline">
                      Printed on your cup and pickup ticket.
                    </span>
                  </div>

                  <div className="mt-1">
                    <label className="font-label-sm text-xs text-on-surface-variant" htmlFor="customer-phone">
                      Phone Number <span className="text-xs text-outline">(Optional)</span>
                    </label>
                    <input
                      type="tel"
                      id="customer-phone"
                      value={customerPhone}
                      onChange={(e) => setCustomerPhone(e.target.value)}
                      className="form-input w-full bg-surface-container-lowest border border-outline-variant/50 rounded-lg px-3 py-2 text-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary mt-0.5"
                      placeholder="e.g. 9876543210"
                    />
                    <span className="font-body-sm text-[11px] text-outline">
                      Used only if our baristas need to clarify your order.
                    </span>
                  </div>

                  <div className="mt-1">
                    <label className="font-label-sm text-xs text-on-surface-variant" htmlFor="special-notes">
                      Special Instructions <span className="text-xs text-outline">(Optional)</span>
                    </label>
                    <textarea
                      id="special-notes"
                      value={specialNotes}
                      onChange={(e) => setSpecialNotes(e.target.value)}
                      className="form-textarea w-full bg-surface-container-lowest border border-outline-variant/50 rounded-lg px-3 py-2 text-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary mt-0.5"
                      rows={2}
                      placeholder="e.g. Extra hot, oat milk"
                    />
                  </div>
                </div>

                {/* Order Summary */}
                <div className="bg-surface-container-low rounded-xl p-space-md flex flex-col gap-space-xs border border-outline-variant/20 mt-space-xs">
                  <div className="flex justify-between text-sm">
                    <span className="text-on-surface-variant">Items</span>
                    <span id="cart-count-summary" className="font-code-pill font-medium">
                      {cartCount} {cartCount === 1 ? 'item' : 'items'}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-on-surface-variant">Subtotal</span>
                    <span id="cart-subtotal" className="font-code-pill font-semibold">
                      {Cart.formatPrice(cartTotal)}
                    </span>
                  </div>
                  <div className="flex justify-between text-xs text-outline">
                    <span>Taxes</span>
                    <span>Included in price</span>
                  </div>
                  <div className="pt-space-xs border-t border-outline-variant/30 flex justify-between items-baseline">
                    <span className="font-headline-sm text-headline-sm text-on-surface">Total Amount</span>
                    <span id="cart-total" className="font-headline-sm text-headline-sm text-primary font-bold">
                      {Cart.formatPrice(cartTotal)}
                    </span>
                  </div>
                </div>

                {/* Demo Notice & Submit */}
                <div className="text-xs text-on-surface-variant bg-surface-container-low p-2 rounded-lg text-center">
                  This is a demo checkout. No payment details are needed online.
                </div>

                <button
                  type="submit"
                  id="btn-place-order"
                  className="w-full bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md py-space-sm px-space-lg rounded-full shadow-md transition-all duration-200 flex items-center justify-center gap-space-xs cursor-pointer"
                >
                  <span>Place Demo Order</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
