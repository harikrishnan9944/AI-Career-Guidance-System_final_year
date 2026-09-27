// CareerPath AI - Main JavaScript Engine

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // 2. Multi-Step Onboarding Form Wizard
    const onboardingForm = document.getElementById('onboardingForm');
    if (onboardingForm) {
        let currentStep = 1;
        const totalSteps = 7;

        const btnNext = document.getElementById('btnNextStep');
        const btnPrev = document.getElementById('btnPrevStep');
        const btnSubmit = document.getElementById('btnSubmitForm');

        function showStep(step) {
            for (let i = 1; i <= totalSteps; i++) {
                const stepPane = document.getElementById(`step-pane-${i}`);
                const stepIndicator = document.getElementById(`step-indicator-${i}`);

                if (stepPane) {
                    if (i === step) {
                        stepPane.classList.remove('d-none');
                    } else {
                        stepPane.classList.add('d-none');
                    }
                }

                if (stepIndicator) {
                    if (i < step) {
                        stepIndicator.classList.add('completed');
                        stepIndicator.classList.remove('active');
                    } else if (i === step) {
                        stepIndicator.classList.add('active');
                        stepIndicator.classList.remove('completed');
                    } else {
                        stepIndicator.classList.remove('active', 'completed');
                    }
                }
            }

            // Button visibility
            if (btnPrev) {
                btnPrev.classList.toggle('d-none', step === 1);
            }

            if (btnNext && btnSubmit) {
                if (step === totalSteps) {
                    btnNext.classList.add('d-none');
                    btnSubmit.classList.remove('d-none');
                } else {
                    btnNext.classList.remove('d-none');
                    btnSubmit.classList.add('d-none');
                }
            }
        }

        if (btnNext) {
            btnNext.addEventListener('click', function () {
                if (validateCurrentStep(currentStep)) {
                    if (currentStep < totalSteps) {
                        currentStep++;
                        showStep(currentStep);
                        window.scrollTo({ top: 100, behavior: 'smooth' });
                    }
                }
            });
        }

        if (btnPrev) {
            btnPrev.addEventListener('click', function () {
                if (currentStep > 1) {
                    currentStep--;
                    showStep(currentStep);
                    window.scrollTo({ top: 100, behavior: 'smooth' });
                }
            });
        }

        function validateCurrentStep(step) {
            if (step === 1) {
                const qual = document.getElementById('qualification');
                const deg = document.getElementById('degree');
                if (qual && !qual.value) {
                    alert('Please select your highest qualification.');
                    return false;
                }
                if (deg && !deg.value.trim()) {
                    alert('Please enter your degree name (e.g. B.Sc Computer Science).');
                    return false;
                }
            }
            return true;
        }

        // Initialize first step
        showStep(currentStep);
    }
});

// Chart.js initialization helper
function createChart(canvasId, chartType, labels, data, labelName, bgColors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: labelName,
                data: data,
                backgroundColor: bgColors || [
                    '#4f46e5', '#2563eb', '#0284c7', '#0d9488', '#059669', '#d97706', '#dc2626'
                ],
                borderRadius: chartType === 'bar' ? 6 : 0,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: chartType !== 'bar',
                    position: 'bottom'
                }
            },
            scales: chartType === 'bar' ? {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 }
                }
            } : {}
        }
    });
}
