// Manejo de submit AJAX para formularios en modales
// Solo aplica si el formulario está dentro de un modal cargado por AJAX


document.addEventListener('submit', async function(e) {
  const form = e.target;
  if (!form.closest('[data-modal-root]')) return;
  e.preventDefault();
  const url = form.getAttribute('action') || window.location.href;
  const method = form.getAttribute('method') || 'post';
  const target = form.closest('[data-modal-root]');
  const formData = new FormData(form);
  try {
    const resp = await fetch(url, {
      method: method.toUpperCase(),
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      body: formData
    });
    const html = await resp.text();
    // Validar que el HTML retornado contiene un modal
    if (/<div[^>]*data-modal-root/.test(html)) {
      target.outerHTML = html;
    } else {
      // Si no es modal, recargar la página principal
      window.location.reload();
    }
  } catch (err) {
    console.error('Error en submit AJAX modal:', err);
  }
});
