document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const url = document.getElementById('urlInput').value.trim();
    if (!url) {
        alert('Please enter a valid URL.');
        return;
    }

    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const jsonOutput = document.getElementById('jsonOutput');

    loading.style.display = 'block';
    results.style.display = 'none';
    jsonOutput.textContent = '';

    try {
        const response = await fetch(`/analyze?url=${encodeURIComponent(url)}`);
        const data = await response.json();

        loading.style.display = 'none';
        results.style.display = 'block';

        displayScoreCards(data.scores);
        displayCharts(data.scores);
        jsonOutput.textContent = JSON.stringify(data, null, 2);

    } catch (error) {
        loading.style.display = 'none';
        alert('Error analyzing the site. Please check the URL and try again.');
        console.error(error);
    }
});

function displayScoreCards(scores) {
    const container = document.getElementById('scoreCards');
    container.innerHTML = '';

    const labels = {
        performance: 'Performance',
        security: 'Security',
        seo: 'SEO',
        accessibility: 'Accessibility',
        best_practices: 'Best Practices',
        eco_score: 'Eco Score',
        broken_links: 'Broken Links',
        mobile_friendly: 'Mobile Friendly'
    };

    for (const [key, value] of Object.entries(scores)) {
        const card = document.createElement('div');
        card.className = 'card';

        let statusClass = 'average';
        if (value >= 80) statusClass = 'excellent';
        else if (value >= 60) statusClass = 'good';
        else if (value >= 40) statusClass = 'average';
        else statusClass = 'poor';

        card.classList.add(statusClass);
        card.innerHTML = `
            <div class="label">${labels[key] || key}</div>
            <div class="value">${value.toFixed(1)}</div>
        `;
        container.appendChild(card);
    }
}

function displayCharts(scores) {
    const labels = [
        'Performance', 'Security', 'SEO', 'Accessibility',
        'Best Practices', 'Eco Score', 'Broken Links', 'Mobile Friendly'
    ];
    const data = Object.values(scores);

    // Radar Chart
    const ctxRadar = document.getElementById('radarChart').getContext('2d');
    new Chart(ctxRadar, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'OmniScope Scores',
                data: data,
                backgroundColor: 'rgba(88, 166, 255, 0.2)',
                borderColor: '#58a6ff',
                pointBackgroundColor: '#58a6ff',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#58a6ff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    min: 0,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        color: '#8b949e'
                    },
                    grid: {
                        color: '#30363d'
                    },
                    pointLabels: {
                        color: '#c9d1d9'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#c9d1d9'
                    }
                }
            }
        }
    });

    // Bar Chart
    const ctxBar = document.getElementById('barChart').getContext('2d');
    new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Scores',
                data: data,
                backgroundColor: [
                    '#f0883e', '#d29922', '#3fb950', '#58a6ff',
                    '#f85149', '#7ee787', '#ff7b72', '#79c0ff'
                ],
                borderColor: '#30363d',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    ticks: {
                        color: '#8b949e'
                    },
                    grid: {
                        color: '#30363d'
                    }
                },
                x: {
                    ticks: {
                        color: '#8b949e',
                        maxRotation: 45,
                        minRotation: 30
                    },
                    grid: {
                        color: '#30363d'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#c9d1d9'
                    }
                }
            }
        }
    });
}

// Sayfa yüklendiğinde varsayılan URL'yi analiz et
window.addEventListener('load', () => {
    document.getElementById('analyzeBtn').click();
});
