'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import confetti from 'canvas-confetti';

function formatDisplayPickupTime(val) {
  if (!val || typeof val !== 'string') return '';
  const trimmed = val.trim();
  if (/^(\d{1,2}):(\d{2})\s*(AM|PM)$/i.test(trimmed)) {
    return trimmed.replace(/\s+(am|pm)$/i, (_, p) => ' ' + p.toUpperCase());
  }
  const match24 = trimmed.match(/^(\d{1,2}):(\d{2})$/);
  if (match24) {
    const hours24 = parseInt(match24[1], 10);
    const mins = match24[2];
    const period = hours24 >= 12 ? 'PM' : 'AM';
    const hours12 = hours24 % 12 === 0 ? 12 : hours24 % 12;
    return `${hours12}:${mins} ${period}`;
  }
  return trimmed;
}

export default function ConfirmationPage() {
  const router = useRouter();
  const [order, setOrder] = useState(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    try {
      const raw = localStorage.getItem('kgp_active_order');
      if (!raw) {
        router.replace('/menu');
        return;
      }
      const parsed = JSON.parse(raw);
      setOrder(parsed);
      setLoaded(true);
      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.6 },
      });
    } catch (e) {
      console.error('Invalid order data', e);
      router.replace('/menu');
    }
  }, [router]);

  const handleOrderAnother = () => {
    localStorage.removeItem('kgp_active_order');
    router.push('/menu');
  };

  const handleCancelOrder = () => {
    if (confirm('Are you sure you want to cancel this demo order?')) {
      localStorage.removeItem('kgp_active_order');
      alert('Demo order cancelled.');
      router.push('/menu');
    }
  };

  if (!loaded || !order) {
    return (
      <div className="w-full min-h-[50vh] flex items-center justify-center">
        <p className="font-body-md text-on-surface-variant">Loading order confirmation...</p>
      </div>
    );
  }

  return (
    <div className="w-full bg-background min-h-[calc(100vh-20rem)] flex items-center justify-center py-space-xl">
      <div className="max-w-xl w-full mx-auto px-margin">
        <div className="bg-surface-container-lowest rounded-2xl shadow-xl p-space-xl border border-outline-variant/30 flex flex-col gap-space-md text-center relative overflow-hidden">
          <div className="w-16 h-16 rounded-full bg-tertiary-fixed text-on-tertiary-fixed flex items-center justify-center mx-auto text-3xl shadow-sm">
            ✓
          </div>

          <div>
            <span className="font-label-sm text-xs uppercase tracking-wider text-primary font-semibold">
              Order Received
            </span>
            <h1 className="font-headline-lg text-headline-lg text-on-surface mt-1">Order Confirmed!</h1>
            <p className="font-body-md text-on-surface-variant mt-1">
              Your order is being prepared fresh by our baristas.
            </p>
          </div>

          {/* Ticket Receipt Box */}
          <div className="bg-surface-container-low rounded-xl p-space-lg text-left border border-outline-variant/20 flex flex-col gap-space-sm font-code-pill text-sm">
            <div className="flex justify-between items-center pb-space-xs border-b border-outline-variant/20">
              <span className="text-outline">Order Ticket</span>
              <span id="ticket-number" className="text-primary font-bold text-base">
                {order.orderNumber}
              </span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-outline">Customer</span>
              <span id="ticket-customer" className="text-on-surface font-semibold">
                {order.customerName}
              </span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-outline">Pickup Time</span>
              <span id="ticket-pickup-time" className="text-tertiary font-bold">
                {formatDisplayPickupTime(order.pickupTime)}
              </span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-outline">Outlet</span>
              <span id="ticket-outlet" className="text-on-surface font-semibold">
                {order.outletName}
              </span>
            </div>

            <div id="ticket-address" className="text-xs text-outline text-right">
              {order.outletAddress}
            </div>

            <ul id="ticket-items-container" className="flex flex-col gap-1 py-1 border-y border-outline-variant/20 text-xs text-on-surface">
              {order.items &&
                order.items.map((it, idx) => {
                  const itemSubtotal = '$' + (Number(it.price) * Number(it.quantity)).toFixed(2);
                  return (
                    <li key={idx} className="ticket-item-row flex justify-between">
                      <span>
                        <strong>{it.quantity}×</strong> {it.name}
                      </span>
                      <span>{itemSubtotal}</span>
                    </li>
                  );
                })}
            </ul>

            {order.specialNotes && order.specialNotes !== 'None' && (
              <div id="ticket-notes" className="text-xs text-secondary italic pt-1 border-t border-outline-variant/20">
                Special Instructions: {order.specialNotes}
              </div>
            )}

            <div className="pt-space-xs border-t border-outline-variant/30 flex justify-between items-baseline">
              <span className="font-label-md font-bold text-on-surface">Total</span>
              <span id="ticket-total" className="font-headline-sm text-primary font-bold">
                {order.total}
              </span>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-space-sm mt-space-sm">
            <button
              type="button"
              id="btn-another-order"
              onClick={handleOrderAnother}
              className="flex-1 bg-primary hover:bg-primary-container text-on-primary font-label-md text-sm py-2.5 rounded-full shadow-sm transition-all text-center cursor-pointer"
            >
              Order Something Else
            </button>
            <Link
              href="/"
              className="flex-1 bg-surface-container-low hover:bg-surface-container text-on-surface font-label-md text-sm py-2.5 rounded-full transition-all text-center"
            >
              Back to Home
            </Link>
          </div>

          <div className="mt-2 text-center">
            <button
              type="button"
              id="btn-cancel-order"
              onClick={handleCancelOrder}
              className="text-xs text-error hover:underline cursor-pointer"
            >
              Cancel Demo Order
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
