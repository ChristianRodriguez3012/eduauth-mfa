document.getElementById('form-login-mfa').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/auth/login-mfa', { email: f.email.value, code: f.code.value });
  const outBox = document.getElementById('out-login-mfa');
  const tokenBox = document.getElementById('token-box');

  if (out.access_token) {
    const bearer = "Bearer " + out.access_token;
    const perfil = await call('/user/profile', {}, { method: 'GET', auth: bearer });

    if (perfil.role === 'admin') {
      localStorage.setItem('admin_token', bearer);
      showAlert('success', 'Login como admin exitoso. Redirigiendo...');
      window.location.href = '/static/admin.html';
      return;
    }

    outBox.innerText = "Token generado con éxito. Cópialo y pégalo en el paso 6 ↓";
    tokenBox.style.display = 'block';
    tokenBox.innerText = bearer;
    document.querySelector('#form-profile input[name="token"]').value = bearer;
    document.querySelector('#form-login-attempts input[name="token"]').value = bearer;
    showAlert('success', 'Login MFA correcto');
  } else {
    outBox.innerText = JSON.stringify(out, null, 2);
    tokenBox.style.display = 'none';
    showAlert('error', 'Error en Login MFA');
  }
};
