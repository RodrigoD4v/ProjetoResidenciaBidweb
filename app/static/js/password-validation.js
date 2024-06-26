document.addEventListener('DOMContentLoaded', () => {
  const passwordInput = document.getElementById('password1');
  if (!passwordInput) {
      console.error('Element with ID "password1" not found!');
      return;
  }

  const charCount = document.getElementById('char-count');
  const uppercaseLowercase = document.getElementById('uppercase-lowercase');
  const number = document.getElementById('number');
  const specialChar = document.getElementById('special-char');
  const notEmail = document.getElementById('not-email');
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  passwordInput.addEventListener('input', () => {
      const value = passwordInput.value;
      console.log('Password input:', value);


      if (value.length >= 12) {
          charCount.style.color = 'green';
      } else {
          charCount.style.color = 'red';
      }

      if (/[a-z]/.test(value) && /[A-Z]/.test(value)) {
          uppercaseLowercase.style.color = 'green';
      } else {
          uppercaseLowercase.style.color = 'red';
      }

      if (/\d/.test(value)) {
          number.style.color = 'green';
      } else {
          number.style.color = 'red';
      }

      if (/[!@#\$%\^\&*\)\(+=._-]/.test(value)) {
          specialChar.style.color = 'green';
      } else {
          specialChar.style.color = 'red';
      }

      if (!emailRegex.test(value)) {
          notEmail.style.color = 'green';
      } else {
          notEmail.style.color = 'red';
      }
  });
});