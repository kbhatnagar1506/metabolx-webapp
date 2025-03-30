document.addEventListener('DOMContentLoaded', () => {
    // Get analysis data from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const analysisData = JSON.parse(decodeURIComponent(urlParams.get('data') || '{}'));

    // Update patient information
    updatePatientInfo(analysisData.patientInfo || {});

    // Update analysis date
    const now = new Date();
    document.getElementById('analysisDate').textContent = now.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });

    // Update health score and status
    const healthScore = analysisData.healthScore || 0;
    document.getElementById('healthScore').textContent = healthScore;
    
    const scoreStatus = document.getElementById('scoreStatus');
    if (healthScore >= 80) {
        scoreStatus.textContent = 'Excellent';
        scoreStatus.className = 'status-badge normal';
    } else if (healthScore >= 60) {
        scoreStatus.textContent = 'Good';
        scoreStatus.className = 'status-badge warning';
    } else {
        scoreStatus.textContent = 'Needs Attention';
        scoreStatus.className = 'status-badge critical';
    }

    // Update critical markers with badges
    const criticalMarkers = document.getElementById('criticalMarkers');
    if (analysisData.criticalMarkers?.length > 0) {
        criticalMarkers.innerHTML = analysisData.criticalMarkers.map(marker => `
            <div class="flex items-center justify-between">
                <span class="text-text-primary">${marker}</span>
                <span class="status-badge critical">Critical</span>
            </div>
        `).join('');
    } else {
        criticalMarkers.innerHTML = '<div class="text-text-secondary">No critical markers detected</div>';
    }

    // Update improvement areas with badges
    const improvementAreas = document.getElementById('improvementAreas');
    if (analysisData.improvementAreas?.length > 0) {
        improvementAreas.innerHTML = analysisData.improvementAreas.map(area => `
            <div class="flex items-center justify-between">
                <span class="text-text-primary">${area}</span>
                <span class="status-badge warning">Needs Improvement</span>
            </div>
        `).join('');
    } else {
        improvementAreas.innerHTML = '<div class="text-text-secondary">No improvement areas identified</div>';
    }

    // Update detailed analysis
    document.getElementById('detailedAnalysis').innerHTML = analysisData.detailedAnalysis || '';

    // Render medicine recommendations
    renderMedicineRecommendations(analysisData.medicines);

    // Render metrics chart and table
    if (analysisData.metrics) {
        renderMetricsChart(analysisData.metrics);
        renderMetricsTable(analysisData.metrics);
    }

    // Render metabolism chart and insights
    if (analysisData.metabolism) {
        renderMetabolismChart(analysisData.metabolism);
        renderMetabolismInsights(analysisData.metabolism);
    }

    // Render recommendations
    renderRecommendations(analysisData.recommendations);

    // Render trends chart
    renderTrendsChart(analysisData);
});

function updatePatientInfo(info) {
    const elements = {
        'patientName': info.name || 'N/A',
        'patientAge': info.age || 'N/A',
        'patientGender': info.gender || 'N/A',
        'patientBMI': info.bmi || 'N/A',
        'patientEthnicity': info.ethnicity || 'N/A'
    };

    for (const [id, value] of Object.entries(elements)) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }

    // Update conditions
    const conditionsEl = document.getElementById('patientConditions');
    if (info.conditions?.length > 0) {
        conditionsEl.innerHTML = info.conditions.map(condition => `
            <div class="flex items-center space-x-2">
                <span class="w-2 h-2 rounded-full bg-warning-color"></span>
                <span>${condition.trim()}</span>
            </div>
        `).join('');
    } else {
        conditionsEl.innerHTML = '<div class="text-text-secondary">No conditions reported</div>';
    }

    // Update medications
    const medicationsEl = document.getElementById('patientMedications');
    if (info.medications?.length > 0) {
        medicationsEl.innerHTML = info.medications.map(medication => `
            <div class="flex items-center space-x-2">
                <span class="w-2 h-2 rounded-full bg-accent-color"></span>
                <span>${medication.trim()}</span>
            </div>
        `).join('');
    } else {
        medicationsEl.innerHTML = '<div class="text-text-secondary">No medications reported</div>';
    }

    // Update allergies
    const allergiesEl = document.getElementById('patientAllergies');
    if (info.allergies?.length > 0) {
        allergiesEl.innerHTML = info.allergies.map(allergy => `
            <div class="flex items-center space-x-2">
                <span class="w-2 h-2 rounded-full bg-danger-color"></span>
                <span>${allergy.trim()}</span>
            </div>
        `).join('');
    } else {
        allergiesEl.innerHTML = '<div class="text-text-secondary">No allergies reported</div>';
    }
}

function renderMedicineRecommendations(medicines) {
    if (!medicines || medicines.length === 0) return;

    // Sort medicines by score (should already be sorted from backend)
    const sortedMedicines = medicines;
    
    // Render top medicine with full details
    const topMedicine = sortedMedicines[0];
    document.getElementById('topMedicine').innerHTML = `
        <div class="bg-success-light p-6 rounded-lg border border-success-color">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h4 class="text-xl font-semibold text-success-color">${topMedicine.name}</h4>
                    <div class="mt-1">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-success-color text-white">
                            ${topMedicine.category}
                        </span>
                    </div>
                </div>
                <div class="text-success-color font-semibold text-lg">${topMedicine.score}/100</div>
            </div>
            
            <div class="space-y-4">
                <div>
                    <p class="text-sm text-text-secondary">${topMedicine.description}</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <h5 class="text-sm font-medium text-text-primary mb-2">Primary Use</h5>
                        <p class="text-sm text-text-secondary">${topMedicine.primaryUse}</p>
                    </div>
                    <div>
                        <h5 class="text-sm font-medium text-text-primary mb-2">Mechanism of Action</h5>
                        <p class="text-sm text-text-secondary">${topMedicine.mechanism}</p>
                    </div>
                </div>

                <div>
                    <h5 class="text-sm font-medium text-text-primary mb-2">Recommended Dosage</h5>
                    <p class="text-sm text-text-secondary">${topMedicine.dosage}</p>
                </div>

                ${topMedicine.warnings.length > 0 ? `
                    <div>
                        <h5 class="text-sm font-medium text-danger-color mb-2">Warnings</h5>
                        <ul class="text-sm list-disc list-inside space-y-1 text-danger-color">
                            ${topMedicine.warnings.map(warning => `<li>${warning}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}

                ${topMedicine.interactions.length > 0 ? `
                    <div>
                        <h5 class="text-sm font-medium text-warning-color mb-2">Drug Interactions</h5>
                        <ul class="text-sm list-disc list-inside space-y-1 text-warning-color">
                            ${topMedicine.interactions.map(interaction => `<li>${interaction}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}

                ${topMedicine.sideEffects.length > 0 ? `
                    <div>
                        <h5 class="text-sm font-medium text-text-primary mb-2">Potential Side Effects</h5>
                        <ul class="text-sm list-disc list-inside space-y-1 text-text-secondary">
                            ${topMedicine.sideEffects.map(effect => `<li>${effect}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}

                ${topMedicine.monitoringNeeded.length > 0 ? `
                    <div>
                        <h5 class="text-sm font-medium text-text-primary mb-2">Monitoring Required</h5>
                        <ul class="text-sm list-disc list-inside space-y-1 text-text-secondary">
                            ${topMedicine.monitoringNeeded.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}

                ${topMedicine.alternatives.length > 0 ? `
                    <div>
                        <h5 class="text-sm font-medium text-text-primary mb-2">Alternative Options</h5>
                        <ul class="text-sm list-disc list-inside space-y-1 text-text-secondary">
                            ${topMedicine.alternatives.map(alt => `<li>${alt}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        </div>
    `;

    // Render all other medicines
    document.getElementById('medicineList').innerHTML = sortedMedicines.slice(1).map(medicine => `
        <div class="medicine-card animate-slide-in">
            <div class="flex justify-between items-start mb-3">
                <div>
                    <div class="flex items-center space-x-2">
                        <h4 class="medicine-name">${medicine.name}</h4>
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            ${medicine.category}
                        </span>
                    </div>
                    <p class="medicine-description mt-1">${medicine.description}</p>
                </div>
                <div class="flex items-center">
                    <div class="text-sm font-medium ${getScoreColor(medicine.score)}">
                        ${medicine.score}/100
                    </div>
                </div>
            </div>

            <div class="efficacy-bar">
                <div class="efficacy-fill ${getEfficacyClass(medicine.score)}"
                     style="width: ${medicine.score}%"></div>
            </div>

            <div class="mt-3 space-y-3">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <div class="text-sm font-medium text-text-primary">Recommended Dosage</div>
                        <div class="text-sm text-text-secondary">${medicine.dosage}</div>
                    </div>
                    <div>
                        <div class="text-sm font-medium text-text-primary">Primary Use</div>
                        <div class="text-sm text-text-secondary">${medicine.primaryUse}</div>
                    </div>
                </div>

                ${medicine.warnings.length > 0 ? `
                    <div>
                        <div class="text-sm font-medium text-danger-color">Key Warning</div>
                        <div class="text-sm text-danger-color opacity-80">${medicine.warnings[0]}</div>
                    </div>
                ` : ''}

                ${medicine.interactions.length > 0 ? `
                    <div>
                        <div class="text-sm font-medium text-warning-color">Key Interaction</div>
                        <div class="text-sm text-warning-color opacity-80">${medicine.interactions[0]}</div>
                    </div>
                ` : ''}

                <div class="pt-2">
                    <button onclick="toggleMedicineDetails(this)" class="text-sm text-accent-color hover:text-accent-color-dark focus:outline-none">
                        Show More Details
                    </button>
                    <div class="hidden medicine-details mt-3 space-y-3">
                        ${medicine.mechanism ? `
                            <div>
                                <div class="text-sm font-medium text-text-primary">Mechanism of Action</div>
                                <div class="text-sm text-text-secondary">${medicine.mechanism}</div>
                            </div>
                        ` : ''}

                        ${medicine.sideEffects.length > 0 ? `
                            <div>
                                <div class="text-sm font-medium text-text-primary">Side Effects</div>
                                <ul class="text-sm list-disc list-inside text-text-secondary">
                                    ${medicine.sideEffects.map(effect => `<li>${effect}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}

                        ${medicine.monitoringNeeded.length > 0 ? `
                            <div>
                                <div class="text-sm font-medium text-text-primary">Monitoring Required</div>
                                <ul class="text-sm list-disc list-inside text-text-secondary">
                                    ${medicine.monitoringNeeded.map(item => `<li>${item}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}

                        ${medicine.alternatives.length > 0 ? `
                            <div>
                                <div class="text-sm font-medium text-text-primary">Alternative Options</div>
                                <ul class="text-sm list-disc list-inside text-text-secondary">
                                    ${medicine.alternatives.map(alt => `<li>${alt}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function toggleMedicineDetails(button) {
    const detailsDiv = button.nextElementSibling;
    const isHidden = detailsDiv.classList.contains('hidden');
    
    detailsDiv.classList.toggle('hidden');
    button.textContent = isHidden ? 'Show Less' : 'Show More Details';
}

function renderRecommendations(recommendations) {
    if (!recommendations) return;

    // Render lifestyle recommendations
    const lifestyleEl = document.getElementById('lifestyleRecommendations');
    if (recommendations.lifestyle?.length > 0) {
        lifestyleEl.innerHTML = recommendations.lifestyle.map(item => `<li>${item}</li>`).join('');
    }

    // Render dietary recommendations
    const dietaryEl = document.getElementById('dietaryRecommendations');
    if (recommendations.diet?.length > 0) {
        dietaryEl.innerHTML = recommendations.diet.map(item => `<li>${item}</li>`).join('');
    }

    // Render follow-up recommendations
    const followUpEl = document.getElementById('followUpTests');
    if (recommendations.followUp?.length > 0) {
        followUpEl.innerHTML = recommendations.followUp.map(item => `<li>${item}</li>`).join('');
    }
}

// Utility functions
function getScoreColor(score) {
    if (score >= 80) return 'text-success-color';
    if (score >= 60) return 'text-warning-color';
    return 'text-danger-color';
}

function getEfficacyClass(score) {
    if (score >= 80) return 'high';
    if (score >= 60) return 'medium';
    return 'low';
}

function getEfficacyLabel(score) {
    if (score >= 80) return 'High Efficacy';
    if (score >= 60) return 'Moderate Efficacy';
    return 'Low Efficacy';
}

function toggleMetricsView(view) {
    const chartView = document.getElementById('metricsChart');
    const tableView = document.getElementById('metricsTable');
    
    if (view === 'chart') {
        chartView.classList.remove('hidden');
        tableView.classList.add('hidden');
    } else {
        chartView.classList.add('hidden');
        tableView.classList.remove('hidden');
    }
}

function renderMetricsChart(metrics) {
    const ctx = document.querySelector('#metricsChart canvas').getContext('2d');
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: metrics.map(m => m.name),
            datasets: [{
                label: 'Your Values',
                data: metrics.map(m => m.value),
                borderColor: 'rgb(37, 99, 235)',
                backgroundColor: 'rgba(37, 99, 235, 0.2)'
            }, {
                label: 'Normal Range',
                data: metrics.map(m => m.normalValue),
                borderColor: 'rgb(156, 163, 175)',
                backgroundColor: 'rgba(156, 163, 175, 0.2)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(156, 163, 175, 0.1)'
                    }
                }
            }
        }
    });
}

function renderMetricsTable(metrics) {
    const table = document.getElementById('metricsTable');
    table.innerHTML = `
        <div class="overflow-x-auto">
            <table class="min-w-full">
                <thead>
                    <tr class="border-b border-gray-200">
                        <th class="text-left py-3 px-4 text-sm font-semibold text-text-secondary">Metric</th>
                        <th class="text-right py-3 px-4 text-sm font-semibold text-text-secondary">Your Value</th>
                        <th class="text-right py-3 px-4 text-sm font-semibold text-text-secondary">Normal Range</th>
                        <th class="text-right py-3 px-4 text-sm font-semibold text-text-secondary">Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${metrics.map(metric => `
                        <tr class="border-b border-gray-100">
                            <td class="py-3 px-4 text-text-primary">${metric.name}</td>
                            <td class="text-right py-3 px-4">${metric.value}</td>
                            <td class="text-right py-3 px-4 text-text-secondary">${metric.normalValue}</td>
                            <td class="text-right py-3 px-4">
                                <span class="status-badge ${getMetricStatus(metric)}">${getMetricStatusLabel(metric)}</span>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

function getMetricStatus(metric) {
    const value = parseFloat(metric.value);
    const normalValue = parseFloat(metric.normalValue);
    const threshold = 0.2; // 20% deviation threshold

    if (Math.abs(value - normalValue) <= threshold * normalValue) {
        return 'normal';
    } else if (Math.abs(value - normalValue) <= threshold * 2 * normalValue) {
        return 'warning';
    } else {
        return 'critical';
    }
}

function getMetricStatusLabel(metric) {
    const status = getMetricStatus(metric);
    if (status === 'normal') return 'Normal';
    if (status === 'warning') return 'Monitor';
    return 'Critical';
}

function renderMetabolismChart(metabolism) {
    const ctx = document.getElementById('metabolismChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: metabolism.map(m => m.type),
            datasets: [{
                data: metabolism.map(m => m.percentage),
                backgroundColor: [
                    'rgba(37, 99, 235, 0.8)',
                    'rgba(5, 150, 105, 0.8)',
                    'rgba(217, 119, 6, 0.8)',
                    'rgba(220, 38, 38, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20
                    }
                }
            },
            cutout: '70%'
        }
    });
}

function renderMetabolismInsights(metabolism) {
    const insights = document.getElementById('metabolismInsights');
    const recommendations = document.getElementById('metabolismRecommendations');
    
    // Generate insights based on metabolism data
    const dominantType = metabolism.reduce((a, b) => a.percentage > b.percentage ? a : b);
    
    insights.innerHTML = `
        <p class="text-sm mb-2">Your metabolism profile shows a predominantly <strong>${dominantType.type.toLowerCase()}</strong> pattern.</p>
        <ul class="text-sm list-disc list-inside space-y-1">
            ${metabolism.map(m => `
                <li>${m.type}: ${m.percentage}%</li>
            `).join('')}
        </ul>
    `;
    
    recommendations.innerHTML = `
        <div class="font-medium mb-2">Recommendations</div>
        <ul class="list-disc list-inside space-y-1">
            <li>Adjust diet according to your ${dominantType.type.toLowerCase()} metabolism</li>
            <li>Focus on balanced nutrient intake</li>
            <li>Consider metabolic optimization supplements</li>
        </ul>
    `;
}

function renderTrendsChart(data) {
    // Simulate some trend data
    const previousScore = data.healthScore - Math.floor(Math.random() * 10);
    const projectedScore = Math.min(100, data.healthScore + Math.floor(Math.random() * 15));
    
    document.getElementById('previousScore').textContent = previousScore;
    document.getElementById('currentScore').textContent = data.healthScore;
    document.getElementById('projectedScore').textContent = projectedScore;
    
    const ctx = document.querySelector('#trendsChart canvas').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Previous', 'Current', 'Projected'],
            datasets: [{
                label: 'Health Score Trend',
                data: [previousScore, data.healthScore, projectedScore],
                borderColor: 'rgb(37, 99, 235)',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    grid: {
                        color: 'rgba(156, 163, 175, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
} 