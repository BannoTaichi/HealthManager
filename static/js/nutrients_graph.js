console.log(window.nutrientLabels, window.nutrientValues);
window.addEventListener('DOMContentLoaded', function () {
  if (!window.nutrientLabels || !window.nutrientValues) return;
  const ctx = document.getElementById('nutrientChart').getContext('2d');
  const nutrientData = {
    labels: window.nutrientLabels,
    datasets: [{
      label: '24時間合計',
      data: window.nutrientValues,
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
        'rgba(153, 102, 255, 0.5)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
      ],
      borderWidth: 1
    }]
  };
  const nutrientConfig = {
    type: 'bar',
    data: nutrientData,
    options: {
      scales: {
        y: {
          beginAtZero: true,
          title: { display: true, text: '合計値 [g]' }
        }
      }
    }
  };
  new Chart(ctx, nutrientConfig);
});