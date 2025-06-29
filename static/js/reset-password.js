document.getElementById('form-reset-password').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/recovery/reset-password', {
    token: f.token.value,
    new_password: f.new_password.value
  });
  document.getElementById('out-reset-password').innerText = JSON.stringify(out, null, 2);
  showAlert(out.msg ? 'success' : 'error', out.msg || 'No se pudo resetear');
};
