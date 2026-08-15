document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('installModal');
  const closeBtn = document.querySelector('.close-btn');
  const copyBtn = document.getElementById('copyBtn');
  const modalTitle = document.getElementById('modalTitle');
  const modalCmd = document.getElementById('modalCmd');

  const copyIcon = '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M16 1H4C2.9 1 2 1.9 2 3v14h2V3h12V1zm3 4H8C6.9 5 6 5.9 6 7v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>';

  const cmds = {
    win:   { title: 'Install on Windows', cmd: 'irm https://raw.githubusercontent.com/AmanBanik/Agen/v2-stable/setup.ps1 | iex' },
    mac:   { title: 'Install on macOS',   cmd: 'curl -sSL https://raw.githubusercontent.com/AmanBanik/Agen/v2-stable/install.sh | bash' },
    linux: { title: 'Install on Linux',   cmd: 'curl -sSL https://raw.githubusercontent.com/AmanBanik/Agen/v2-stable/install.sh | bash' }
  };

  document.querySelectorAll('.dl-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const platform = btn.dataset.platform;
      if (!platform) return; // repo link behaves like a normal link
      e.preventDefault();
      modalTitle.textContent = cmds[platform].title;
      modalCmd.textContent = cmds[platform].cmd;
      modal.style.display = 'flex';
      copyBtn.innerHTML = copyIcon;
    });
  });

  closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });
  window.addEventListener('click', (e) => {
    if (e.target === modal) modal.style.display = 'none';
  });

  copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(modalCmd.textContent);
    copyBtn.textContent = 'Copied!';
    setTimeout(() => { copyBtn.innerHTML = copyIcon; }, 1500);
  });

  // Smart sticky navbar logic
  let lastScrollY = window.scrollY;
  const nav = document.querySelector('nav');
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > lastScrollY && window.scrollY > 150) {
      // Scrolling down and past the header
      nav.classList.add('nav-hidden');
    } else {
      // Scrolling up
      nav.classList.remove('nav-hidden');
    }
    lastScrollY = window.scrollY;
  }, { passive: true });
});
