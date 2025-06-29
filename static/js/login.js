document.getElementById('form-login').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const out = await call('/auth/login', {
    email: f.email.value,
    password: f.password.value
  });
  if (out.access_token) {
    showAlert('success', 'Login exitoso. Redirigiendo...');
    window.location.href = 'profile.html';
  } else {
    showAlert('error', out.msg || 'Error al hacer login');
  }
};
