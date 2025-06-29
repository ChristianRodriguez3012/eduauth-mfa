document.getElementById('form-request-reset').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/recovery/request-reset', { email: f.email.value });
  showAlert(out.reset_token ? 'success' : 'warn', out.msg || 'Error al generar token');
};

document.getElementById('form-reset-password').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/recovery/reset-password', {
    token: f.token.value,
    new_password: f.new_password.value
  });
  showAlert(out.msg ? 'success' : 'error', out.msg || 'No se pudo resetear');
};
