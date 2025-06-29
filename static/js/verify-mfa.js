document.getElementById('form-verify-mfa').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/auth/verify-mfa', { email: f.email.value, code: f.code.value });
  document.getElementById('out-verify-mfa').innerText = JSON.stringify(out, null, 2);
  showAlert(out.msg ? 'success' : 'error', out.msg || 'Verificación fallida');
};
