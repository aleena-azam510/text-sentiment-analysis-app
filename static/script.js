document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('sentiment-form');
    const predictButton = document.getElementById('predict-button');
    const loadingSpinner = document.getElementById('loading-spinner');
    const reviewInput = document.getElementById('review-input');

    if (form && predictButton && loadingSpinner && reviewInput) {
        form.addEventListener('submit', () => {
            predictButton.disabled = true;
            predictButton.innerHTML = 'Predicting... <span class="spinner"></span>';
            const spinner = predictButton.querySelector('.spinner');
            if (spinner) {
                spinner.style.display = 'block';
            }
        });

        // Optional: Character counter for the textarea
        const charCountDisplay = document.createElement('div');
        charCountDisplay.id = 'char-count';
        charCountDisplay.style.cssText = `
            font-size: 0.9em;
            color: #888;
            margin-top: 10px;
            text-align: right;
            padding-right: 10%;
        `;
        reviewInput.parentNode.insertBefore(charCountDisplay, reviewInput.nextSibling);

        reviewInput.addEventListener('input', () => {
            const currentLength = reviewInput.value.length;
            charCountDisplay.textContent = `${currentLength} characters`;
            if (currentLength > 500) { // Example limit
                charCountDisplay.style.color = 'red';
            } else {
                charCountDisplay.style.color = '#888';
            }
        });
        reviewInput.dispatchEvent(new Event('input')); // Initialize count on load
    }
});