/* Work filter (home) and resume print button. */
(function(){
  const list = document.getElementById('work-list');
  if (list){
    const filters = document.getElementById('filters'), status = document.getElementById('filter-status'), empty = document.getElementById('work-empty');
    const tidy = () => {
      const items = [...list.querySelectorAll('.work-item')], shown = items.filter(li => !li.hidden);
      items.forEach(li => li.classList.remove('tail'));
      const after = shown[0] === items[0] ? shown.length - 1 : shown.length;
      list.classList.toggle('even-tail', after % 2 === 1 && after > 1);
      if (after % 2 === 1 && after > 1) shown[shown.length - 1].classList.add('tail');
    };
    tidy();
    filters.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      filters.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      const role = b.dataset.role; let n = 0;
      list.querySelectorAll('.work-item').forEach(li => { const show = !role || li.dataset.roles.split('|').includes(role); li.hidden = !show; if (show) n++; });
      empty.hidden = n > 0; tidy();
      status.textContent = role ? `Showing ${n} project${n === 1 ? '' : 's'} in ${role}` : `Showing all ${n} projects`;
    });
  }
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
