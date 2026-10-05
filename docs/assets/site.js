/* Resume print button. */
(function(){
  const p = document.getElementById('print'); if (p) p.addEventListener('click', () => window.print());
})();

/* Copy-email button: mailto links do nothing when no mail app is set up. */
(function(){
  document.addEventListener('click', e => {
    const b = e.target.closest('.copy-email'); if (!b) return;
    const t = b.dataset.email, label = b.textContent;
    const ok = () => { b.textContent = 'Copied'; setTimeout(() => b.textContent = label, 1600); };
    const fallback = () => { const ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); ok(); } catch (err) { b.textContent = t; } ta.remove(); };
    navigator.clipboard ? navigator.clipboard.writeText(t).then(ok, fallback) : fallback();
  });
})();
