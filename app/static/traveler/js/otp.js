const inputs = document.querySelectorAll('.otp-input');

inputs.forEach((input, index) => {
  // 1. Handle typing forward
  input.addEventListener('input', (e) => {
    const value = e.target.value;
    
    // Ensure only numbers are entered
    if (!/^[0-9]$/.test(value)) {
      e.target.value = '';
      return;
    }

    // Move to the next input if it exists
    if (value && index < inputs.length - 1) {
      inputs[index + 1].focus();
    }
  });

  // 2. Handle backspace to move backward
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Backspace') {
      // If the current field is empty, move focus backward and clear it
      if (!input.value && index > 0) {
        inputs[index - 1].focus();
        inputs[index - 1].value = '';
      }
    }
  });

  // 3. Handle pasting a 6-digit code
  input.addEventListener('paste', (e) => {
    e.preventDefault();
    const pastedData = e.clipboardData.getData('text').trim();

    // Verify the pasted text is exactly 6 digits
    if (/^[0-9]{6}$/.test(pastedData)) {
      inputs.forEach((otpInput, i) => {
        otpInput.value = pastedData[i];
      });
      // Focus the last input box after pasting
      inputs[inputs.length - 1].focus();
    }
  });
});


// COUNTDOWN TIMER
let timeLeft = 30; // Seconds to count down
const counterSpan = document.getElementById('otp-counter');
const timerContainer = document.getElementById('timer-container');
const resendLink = document.getElementById('resend-link');

const countdown = setInterval(() => {
  timeLeft--;

  // Format the numbers so it displays "00:09" instead of "00:9"
  const secondsDisplay = timeLeft < 10 ? `0${timeLeft}` : timeLeft;
  counterSpan.textContent = `00:${secondsDisplay}`;

  // When the timer hits 0
  if (timeLeft <= 0) {
    clearInterval(countdown);
    
    // Change layout states
    timerContainer.classList.add('text-muted'); // Optional: fade out old timer text
    resendLink.classList.remove('d-none');     // Reveal the resend link on the right
  }
}, 1000);

// Submit listener to concatenate digits before form submission
const otpForm = document.querySelector('form');
if (otpForm) {
  otpForm.addEventListener('submit', () => {
    const otpVal = Array.from(inputs).map(input => input.value).join('');
    const hiddenInput = document.getElementById('otp-hidden');
    if (hiddenInput) {
      hiddenInput.value = otpVal;
    }
  });
}

// Function that handles the click event when the user clicks "Resend OTP"
function resendOTP(event) {
  event.preventDefault();
  
  // Submit a POST request to '/request-otp/' programmatically
  const tempForm = document.createElement('form');
  tempForm.method = 'POST';
  tempForm.action = '/request-otp/';
  
  // Find CSRF token inside the current form and clone it to our temporary form
  const csrfInput = document.querySelector('input[name="csrf_token"]');
  if (csrfInput) {
    const clonedCsrf = document.createElement('input');
    clonedCsrf.type = 'hidden';
    clonedCsrf.name = 'csrf_token';
    clonedCsrf.value = csrfInput.value;
    tempForm.appendChild(clonedCsrf);
  }
  
  document.body.appendChild(tempForm);
  tempForm.submit();
}
