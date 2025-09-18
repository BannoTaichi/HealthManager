window.addEventListener('DOMContentLoaded', function() {
  if (!window.stretchLabels || !window.stretchValues) return;
  const ctx = document.getElementById('stretchChart').getContext('2d');
  const stretchData = {
    labels: window.stretchLabels,
    datasets: [{
      data: window.stretchValues,
      backgroundColor: 'rgba(255, 206, 86, 0.5)',
      borderColor: 'rgba(255, 206, 86, 1)',
      borderWidth: 1
    }]
  };
  const stretchConfig = {
    type: 'bar',
    data: stretchData,
    options: {
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  };
  new Chart(ctx, stretchConfig);
});