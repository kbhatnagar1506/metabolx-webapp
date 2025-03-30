document.addEventListener('DOMContentLoaded', () => {
    const textReport = document.getElementById('textReport');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const textAnalysisResult = document.getElementById('textAnalysisResult');
    const medicineList = document.getElementById('medicineList');

    // Handle form submission
    analyzeBtn.addEventListener('click', async () => {
        const text = textReport.value.trim();

        if (!text) {
            alert('Please enter your blood report text');
            return;
        }

        loading.style.display = 'block';
        results.style.display = 'none';

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text_report: text
                })
            });

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            if (data.redirect) {
                window.location.href = data.redirect;
            }
        } catch (error) {
            alert('Error analyzing report: ' + error.message);
            loading.style.display = 'none';
            results.style.display = 'block';
        }
    });

    function displayResults(data) {
        if (data.analysis) {
            // Display the analysis text directly without trying to parse JSON
            textAnalysisResult.innerHTML = `
                <div class="analysis-content">
                    <p>${data.analysis}</p>
                </div>
            `;
            medicineList.innerHTML = ''; // Clear medicine list as we're not using structured data
        }
    }
}); 