// Handler para cerrar modales al hacer clic en el botón X (data-close-modal)
document.addEventListener('click', function(e) {
  const btn = e.target.closest('[data-close-modal]');
  if (!btn) return;
  e.preventDefault();
  // Busca el modal más cercano (data-modal-root)
  const modal = btn.closest('[data-modal-root]');
  if (modal) {
    modal.remove();
    document.dispatchEvent(new CustomEvent('modal:close'));
  }
});

// Handler global para botón CANCELAR en cualquier modal
document.addEventListener('click', async function(e) {
  const btn = e.target.closest('#btnCancelarEliminar');
  if (!btn) return;
  e.preventDefault();
  // Cerrar el modal actual
  const modal = btn.closest('[data-modal-root]');
  if (modal) modal.remove();
  // Recargar listado en el contenedor
  const container = document.querySelector('#app-modal-container');
  if (container) {
    const resp = await fetch(container.getAttribute('data-list-url') || '/empleados/', {
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    });
    const html = await resp.text();
    container.innerHTML = html;
  }
});
