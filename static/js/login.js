const form = document.querySelector('form');
const recaptchaError = document.getElementById('recaptcha-error');
form.addEventListener('submit', (e) => {
            e.preventDefault();
            const captchaResponse = grecaptcha.getResponse();
    
            if (captchaResponse.length > 0) {
                recaptchaError.style.display = 'none'; 
                form.submit();
            } else {
                recaptchaError.style.display = 'block';
            }
        });
function googleTranslateElementInit() {
            new google.translate.TranslateElement({ pageLanguage: 'en' }, 'google_translate_element');
}
        