document.getElementById('form-register').onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const role = f.role.value;
  const email = f.email.value.trim();
  const password = f.password.value.trim();
  const dni = f.dni.value.trim();

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    showAlert('warn', '⚠️ Ingresa un email válido');
    return;
  }

  if (!/^(?=.*[a-zA-Z])(?=.*\d).{6,}$/.test(password)) {
    showAlert('warn', '⚠️ La contraseña debe tener al menos 6 caracteres, incluyendo letras y números');
    return;
  }

  if (['admin', 'profesor'].includes(role)) {
    if (!/^\d{8}$/.test(dni)) {
      showAlert('warn', '⚠️ El DNI debe tener exactamente 8 dígitos');
      return;
    }
  }

  const payload = { email, password, role };
  if (dni) payload.dni = dni;

  const out = await call('/auth/register', payload);
  showAlert(out.msg?.includes("existe") ? 'warn' : 'success', out.msg || 'Registro fallido');
};

// Mostrar u ocultar campo DNI según el rol
const roleSelector = document.getElementById('role');
const dniField = document.getElementById('dni');
roleSelector.onchange = () => {
  const rol = roleSelector.value;
  dniField.style.display = ['admin', 'profesor'].includes(rol) ? 'block' : 'none';
};
