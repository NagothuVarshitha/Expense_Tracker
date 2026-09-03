const chartCanvas = document.getElementById('categoryChart');
if (chartCanvas && window.categoryData) {
  new Chart(chartCanvas, {
    type: 'doughnut',
    data: { labels: window.categoryData.labels, datasets: [{ data: window.categoryData.values, backgroundColor: ['#087f8c', '#ef806b', '#f4c95d', '#7d9db2', '#86c7b4', '#d49a89', '#5f7a89', '#bdd5ce'], borderWidth: 0 }] },
    options: { responsive: true, cutout: '68%', plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, padding: 18, font: { family: 'DM Sans' } } }, tooltip: { callbacks: { label: (context) => ` ₹${Number(context.raw).toLocaleString('en-IN')}` } } } }
  });
}
