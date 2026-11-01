/**
 * confirmation.js
 * Renders the persistent order ticket from localStorage and handles re-ordering / cancellation.
 */

document.addEventListener('DOMContentLoaded', () => {
  const orderRaw = localStorage.getItem('kgp_active_order');
  
  // If visited without an active order, redirect to menu
  if (!orderRaw) {
    window.location.replace('menu.html');
    return;
  }

  let order;
  try {
    order = JSON.parse(orderRaw);
  } catch (e) {
    console.error("Invalid order data", e);
    window.location.replace('menu.html');
    return;
  }

  // Populate Ticket Elements
  const ticketNumEl = document.getElementById('ticket-number');
  const customerNameEl = document.getElementById('ticket-customer');
  const pickupTimeEl = document.getElementById('ticket-pickup-time');
  const outletNameEl = document.getElementById('ticket-outlet');
  const outletAddrEl = document.getElementById('ticket-address');
  const itemsContainer = document.getElementById('ticket-items-container');
  const ticketTotalEl = document.getElementById('ticket-total');
  const ticketNotesEl = document.getElementById('ticket-notes');

  // Format a pickup time string into 12-hour "h:mm AM/PM" if needed
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

  if (ticketNumEl) ticketNumEl.textContent = order.orderNumber;
  if (customerNameEl) customerNameEl.textContent = order.customerName;
  if (pickupTimeEl) pickupTimeEl.textContent = formatDisplayPickupTime(order.pickupTime);
  if (outletNameEl) outletNameEl.textContent = order.outletName;
  if (outletAddrEl) outletAddrEl.textContent = order.outletAddress;
  if (ticketTotalEl) ticketTotalEl.textContent = order.total;

  if (ticketNotesEl && order.specialNotes && order.specialNotes !== 'None') {
    ticketNotesEl.textContent = `Special Instructions: ${order.specialNotes}`;
    ticketNotesEl.style.display = 'block';
  }

  // Populate Items
  if (itemsContainer && Array.isArray(order.items)) {
    itemsContainer.innerHTML = '';
    order.items.forEach(item => {
      const row = document.createElement('li');
      row.className = 'ticket-item-row';
      const itemSubtotal = '$' + (Number(item.price) * Number(item.quantity)).toFixed(2);
      row.innerHTML = `
        <span><strong>${item.quantity}×</strong> ${item.name}</span>
        <span>${itemSubtotal}</span>
      `;
      itemsContainer.appendChild(row);
    });
  }

  // Button: Place Another Order
  const btnAnother = document.getElementById('btn-another-order');
  if (btnAnother) {
    btnAnother.addEventListener('click', () => {
      localStorage.removeItem('kgp_active_order');
      window.location.href = 'menu.html';
    });
  }

  // Button: Cancel Demo Order
  const btnCancel = document.getElementById('btn-cancel-order');
  if (btnCancel) {
    btnCancel.addEventListener('click', () => {
      const confirmed = confirm("Are you sure you want to cancel this demo order?");
      if (confirmed) {
        localStorage.removeItem('kgp_active_order');
        alert("Demo order cancelled.");
        window.location.href = 'menu.html';
      }
    });
  }
});
