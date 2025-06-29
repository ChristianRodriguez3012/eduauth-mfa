const API = window.location.origin;

function showAlert(type, msg) {
  const box = document.getElementById('alert');
  box.className = 'alert ' + type;
  const prefix = { success: '✅ ', error: '❌ ', warn: '⚠️ ' }[type] || '';
  box.innerText = prefix + msg;
  box.style.display = 'block';
  clearTimeout(box.timeout);
  box.timeout = setTimeout(() => box.style.display = 'none', 5000);
}

async function call(endpoint, data, opts = {}) {
  const res = await fetch(API + endpoint, {
    method: opts.method || 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(opts.auth ? { 'Authorization': opts.auth } : {})
    },
    body: ['GET'].includes(opts.method) ? null : JSON.stringify(data)
  });
  const txt = await res.text();
  try { return JSON.parse(txt); } catch { return txt; }
}
