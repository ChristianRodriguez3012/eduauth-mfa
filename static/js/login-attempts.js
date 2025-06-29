document.getElementById('form-login-attempts').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/user/login-attempts', {}, { method: 'GET', auth: f.token.value });
  document.getElementById('out-login-attempts').innerText = JSON.stringify(out, null, 2);
  showAlert(Array.isArray(out) ? 'success' : 'error', Array.isArray(out) ? 'Historial obtenido' : (out.msg || 'Error'));
};
