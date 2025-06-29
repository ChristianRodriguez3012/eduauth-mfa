document.getElementById('form-request-reset').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/recovery/request-reset', { email: f.email.value });
  document.getElementById('out-request-reset').innerText = JSON.stringify(out, null, 2);
  showAlert(out.reset_token ? 'success' : 'warn', out.msg || 'Error al generar token');
};
