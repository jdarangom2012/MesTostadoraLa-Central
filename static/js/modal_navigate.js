// Handler genérico para navegación AJAX de modales
// No interfiere con otros modales existentes

document.addEventListener('click', async (e) => {
  const a = e.target.closest('[data-modal-navigate="true"]');
  if (!a) return;
  e.preventDefault();
  const url = a.getAttribute('href');
  const targetSel = a.getAttribute('data-modal-target') || '#app-modal-container';
  const target = document.querySelector(targetSel);
  if (!url || !target) return;

  try {
    const resp = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' }});
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    const html = await resp.text();
    target.innerHTML = html;
    // Si el proyecto usa una función global para abrir modales, invócala aquí.
    if (window.showModal) window.showModal(target);
    else {
      // fallback: si es <dialog>:
      const dlg = target.querySelector('dialog') || target;
      if (dlg.showModal) dlg.showModal();
      // si usa lib distinta, dispara el evento estándar que ya usan los demás modales:
      target.dispatchEvent(new CustomEvent('modal:open'));
    }
  } catch (err) {
    console.error('Error cargando modal:', err);
  }
}, true);
