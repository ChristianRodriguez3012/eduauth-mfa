document.getElementById('form-setup-mfa').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/auth/setup-mfa', { email: f.email.value });
  document.getElementById('qr-img').src = out.qr_code || '';
  showAlert(out.qr_code ? 'success' : 'error', out.qr_code ? 'QR generado' : 'Error generando QR');
};

document.getElementById('form-verify-mfa').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/auth/verify-mfa', { email: f.email.value, code: f.code.value });
  showAlert(out.msg ? 'success' : 'error', out.msg || 'Verificación fallida');
};

document.getElementById('form-login-mfa').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/auth/login-mfa', { email: f.email.value, code: f.code.value });
  const tokenBox = document.getElementById('token-box');

  if (out.access_token) {
    const bearer = "Bearer " + out.access_token;
    const perfil = await call('/user/profile', {}, { method: 'GET', auth: bearer });

    if (perfil.role === 'admin') {
      localStorage.setItem('admin_token', bearer);
      showAlert('success', 'Login admin exitoso');
      window.location.href = '/static/admin.html';
    } else {
      showAlert('success', 'Login MFA exitoso');
      tokenBox.style.display = 'block';
      tokenBox.innerText = bearer;
      localStorage.setItem('user_token', bearer);
      setTimeout(() => window.location.href = 'profile.html', 2000);
    }
  } else {
    showAlert('error', 'Error en login MFA');
    tokenBox.style.display = 'none';
  }
};
