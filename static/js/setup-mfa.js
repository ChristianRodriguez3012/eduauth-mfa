document.getElementById('form-setup-mfa').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/auth/setup-mfa', { email: f.email.value });
  document.getElementById('qr-img').src = out.qr_code || '';
  document.getElementById('out-setup-mfa').innerText = JSON.stringify(out, null, 2);
  showAlert(out.qr_code ? 'success' : 'error', out.qr_code ? 'QR generado' : 'Error generando QR');
};
