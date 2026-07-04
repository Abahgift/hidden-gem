/* ── ONBOARDING ── */
  function obNext(step) {
    document.getElementById('ob-step-' + step).style.display = 'none';
    document.getElementById('ob-step-' + (step+1)).style.display = 'block';
    updateStepBar(step+1);
  }
  function obBack(step) {
    document.getElementById('ob-step-' + step).style.display = 'none';
    document.getElementById('ob-step-' + (step-1)).style.display = 'block';
    updateStepBar(step-1);
  }
  function updateStepBar(current) {
    const bars = document.querySelectorAll('#ob-steps div');
    bars.forEach((b,i) => {
      b.className = '';
      if (i < current-1) b.className = 'done';
      else if (i === current-1) b.className = 'active';
    });
  }
  function goApp() {
    showScreen('app');
    showToast('Profile submitted — pending admin review');
  }
  function showScreen(id) {
    const target = document.getElementById(id);
    if (!target && id === 'onboarding') {
      window.location.href = 'sign_out.html';
      return;
    }
    if (!target && id === 'app') {
      window.location.href = 'dashboard.html';
      return;
    }
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    if (target) target.classList.add('active');
  }
  function toggleTag(el) { el.classList.toggle('selected'); }
  function toggleDay(el) { el.classList.toggle('selected'); }

  /* ── NAV ── */
  function switchTab(name, el) {
    const panel = document.getElementById('tab-' + name);
    if (!panel) {
      const pageMap = {
        dashboard: 'dashboard.html',
        bookings: 'bookings.html',
        trails: 'my_trails.html',
        reviews: 'reviews.html',
        profile: 'my_profile.html'
      };
      if (pageMap[name]) window.location.href = pageMap[name];
      return;
    }
    document.querySelectorAll('.tab-panel').forEach(t => t.classList.remove('active'));
    panel.classList.add('active');
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    if (el) el.classList.add('active');
  }

  /* ── BOOKINGS ── */
  function filterBookings(status, btn) {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.booking-card').forEach(c => {
      if (status === 'all' || c.dataset.status === status) c.style.display = 'flex';
      else c.style.display = 'none';
    });
  }
  function confirmBooking(btn) {
    const card = btn.closest('.booking-card');
    card.dataset.status = 'confirmed';
    card.querySelector('.status-pill').className = 'status-pill confirmed';
    card.querySelector('.status-pill').textContent = 'Confirmed';
    btn.closest('.booking-actions').innerHTML = '<span class="status-pill confirmed">Confirmed</span>';
    updateBadge();
    showToast('Booking confirmed! Traveler has been notified');
  }
  function declineBooking(btn) {
    const card = btn.closest('.booking-card');
    card.dataset.status = 'cancelled';
    card.querySelector('.status-pill').className = 'status-pill cancelled';
    card.querySelector('.status-pill').textContent = 'Cancelled';
    btn.closest('.booking-actions').innerHTML = '<span class="status-pill cancelled">Cancelled</span>';
    updateBadge();
    showToast('Booking declined.');
  }
  function updateBadge() {
    const pending = document.querySelectorAll('.booking-card[data-status="pending"]').length;
    document.getElementById('booking-badge').textContent = pending;
    if (pending === 0) document.getElementById('booking-badge').style.display = 'none';
  }

  /* ── TRAILS ── */
  function removeTrail(btn) {
    btn.closest('.trail-card').remove();
    showToast('Destination removed from your trails.');
  }
  function openAddTrailModal() {
    document.getElementById('add-trail-modal').classList.add('open');
  }
  function closeModal() {
    document.getElementById('add-trail-modal').classList.remove('open');
  }
  function addTrail(name, loc, icon, diff) {
    closeModal();
    const grid = document.getElementById('trails-grid');
    const diffClass = {Easy:'diff-easy',Moderate:'diff-moderate',Hard:'diff-hard',Extreme:'diff-extreme'}[diff] || 'diff-moderate';
    const card = document.createElement('div');
    card.className = 'trail-card';
    card.innerHTML = `
      <div class="trail-icon"><i class="bi \${icon} text-success"></i></div>
      <div style="flex:1;">
        <div class="trail-name">\${name}</div>
        <div class="trail-loc"><i class="bi bi-geo-alt-fill text-muted"></i> \${loc}</div>
        <div class="trail-tags">
          <span class="diff-pill \${diffClass}">\${diff}</span>
        </div>
      </div>
      <button class="trail-remove" onclick="removeTrail(this)" title="Remove">✕</button>`;
    grid.appendChild(card);
    showToast(name + ' added to your trails');
  }

  /* ── REVIEWS ── */
  function postReply(btn) {
    const area = btn.closest('.reply-input-area');
    const text = area.querySelector('textarea').value.trim();
    if (!text) return;
    const replyDiv = document.createElement('div');
    replyDiv.className = 'review-reply';
    replyDiv.innerHTML = `<div class="review-reply-label">Your reply</div><p>${text}</p>`;
    area.parentNode.replaceChild(replyDiv, area);
    showToast('Reply posted');
  }

  /* ── TOAST ── */
  function showToast(msg) {
    const t = document.getElementById('toast');
    document.getElementById('toast-msg').textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3200);
  }

  /* close modal on overlay click */
  const addTrailModal = document.getElementById('add-trail-modal');
  if (addTrailModal) {
    addTrailModal.addEventListener('click', function(e) {
      if (e.target === this) closeModal();
    });
  }
