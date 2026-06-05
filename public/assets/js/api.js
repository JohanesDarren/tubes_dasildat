document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predict-form');
    const loading = document.getElementById('loading');
    const resultsContainer = document.getElementById('results-container');
    const submitBtn = document.getElementById('submit-btn');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Show loading
            loading.style.display = 'block';
            resultsContainer.style.display = 'none';
            submitBtn.disabled = true;

            const formData = new FormData(form);
            const model = formData.get('model');
            
            // Build features object
            const features = {};
            for (let [key, value] of formData.entries()) {
                if (key !== 'model') {
                    features[key] = parseFloat(value);
                }
            }

            try {
                // Determine API URL based on environment (Vercel vs Local)
                const apiUrl = window.location.hostname.includes('vercel.app') 
                    ? '/api/predict' 
                    : 'http://127.0.0.1:5050/api/predict';

                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        model: model,
                        features: features
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    renderResults(data, model);
                } else {
                    showError(data.error || 'Failed to make prediction.');
                }
            } catch (error) {
                console.error('Error:', error);
                showError('Network error occurred while connecting to the API.');
            } finally {
                loading.style.display = 'none';
                submitBtn.disabled = false;
            }
        });
    }

    function renderResults(data, requestedModel) {
        let html = `
            <div class="results-header" style="text-align: center; margin: 48px 0 32px;">
                <h2>Prediction <span class="gradient-text">Results</span></h2>
                <p>Based on your biosensor input</p>
            </div>
        `;

        if (requestedModel === 'all') {
            html += `<div class="card-grid card-grid-3">`;
            for (const [modelKey, result] of Object.entries(data.predictions)) {
                if (result.success) {
                    html += generateResultCard(result);
                } else {
                    html += `<div class="card"><p class="text-danger">Error in ${modelKey}: ${result.error}</p></div>`;
                }
            }
            html += `</div>`;
        } else {
            html += `<div style="max-width: 600px; margin: 0 auto;">`;
            html += generateResultCard(data);
            html += `</div>`;
        }

        // Input Summary
        const inputs = requestedModel === 'all' 
            ? data.predictions[Object.keys(data.predictions)[0]].input_features 
            : data.input_features;
            
        html += `
            <div class="card animate-on-scroll" style="max-width: 800px; margin: 48px auto 0;">
                <h3 style="font-family: var(--font-display); margin-bottom: 24px;">
                    <i class="fas fa-list" style="color: var(--primary-400);"></i> Input Summary
                </h3>
                <div class="form-grid">
        `;
        
        for (const [key, val] of Object.entries(inputs)) {
            const formattedKey = key.replace(/_/g, ' ');
            html += `
                <div style="padding: 12px; background: rgba(255,255,255,0.02); border-radius: var(--radius-sm); border: 1px solid var(--border-glass);">
                    <div style="font-size: 0.8rem; color: var(--text-muted);">${formattedKey}</div>
                    <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">${val}</div>
                </div>
            `;
        }
        
        html += `</div></div>`;
        
        resultsContainer.innerHTML = html;
        resultsContainer.style.display = 'block';
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function generateResultCard(result) {
        const p = result.prediction;
        let statusClass = '';
        let iconClass = '';
        
        if (p === 'Healthy') {
            statusClass = 'healthy';
            iconClass = 'fa-heart';
        } else if (p === 'Moderate Stress') {
            statusClass = 'moderate';
            iconClass = 'fa-exclamation-triangle';
        } else {
            statusClass = 'stress';
            iconClass = 'fa-times-circle';
        }

        let probsHtml = '';
        const colors = {
            'Healthy': 'var(--status-healthy)',
            'Moderate Stress': 'var(--status-moderate)',
            'High Stress': 'var(--status-stress)'
        };

        for (const [cls, prob] of Object.entries(result.probabilities)) {
            const percent = (prob * 100).toFixed(1);
            probsHtml += `
                <div class="prob-row">
                    <div class="prob-label">
                        <span>${cls}</span>
                        <span>${percent}%</span>
                    </div>
                    <div class="prob-bar-bg">
                        <div class="prob-bar-fill" style="width: ${percent}%; background-color: ${colors[cls]}"></div>
                    </div>
                </div>
            `;
        }

        return `
            <div class="card result-card animate-on-scroll" style="border-top: 4px solid var(--status-${statusClass});">
                <div class="result-header">
                    <h4>${result.model_name}</h4>
                </div>
                <div class="result-status status-${statusClass}">
                    <i class="fas ${iconClass} result-icon"></i>
                    <h2>${p}</h2>
                </div>
                <div class="probabilities">
                    <h5 style="margin-bottom: 12px; color: var(--text-secondary); font-size: 0.9rem;">Class Probabilities</h5>
                    ${probsHtml}
                </div>
            </div>
        `;
    }

    function showError(message) {
        resultsContainer.innerHTML = `
            <div class="alert alert-danger" style="max-width: 600px; margin: 40px auto; text-align: left;">
                <i class="fas fa-exclamation-circle" style="font-size: 1.5rem; margin-bottom: 12px; display: block; color: #ef4444;"></i>
                <h4 style="margin-bottom: 8px;">Prediction Error</h4>
                <p>${message}</p>
            </div>
        `;
        resultsContainer.style.display = 'block';
    }
});
