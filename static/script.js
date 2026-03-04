// Form validation and client-side script
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.bp-form');

    if (form) {
        form.addEventListener('submit', function (e) {
            if (!validateForm()) {
                e.preventDefault();
                showAlert('Please fill in all required fields.', 'error');
            }
        });
    }

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease-in-out';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
});

function validateForm() {
    const form = document.querySelector('.bp-form');
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#ef4444';
            isValid = false;
        } else {
            field.style.borderColor = '#e5e7eb';
        }
    });

    return isValid;
}

function showAlert(message, type) {
    const alertsContainer = document.querySelector('.container');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        <span>${message}</span>
        <button class="close-btn" onclick="this.parentElement.style.display='none';">&times;</button>
    `;
    alertsContainer.insertBefore(alertDiv, alertsContainer.firstChild);

    setTimeout(() => {
        alertDiv.style.display = 'none';
    }, 5000);
}

// Prevent form submission if validation fails
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.bp-form');
    if (form) {
        form.addEventListener('submit', function (e) {
            const requiredFields = form.querySelectorAll('select[required], input[type="text"][required]');
            let allFilled = true;

            requiredFields.forEach(field => {
                if (!field.value) {
                    allFilled = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });

            if (!allFilled) {
                e.preventDefault();
            }
        });
    }
});
