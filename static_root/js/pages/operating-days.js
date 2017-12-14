
$(function () {
    new Chart(document.getElementById("line_chart").getContext("2d"), getChartJs());
});

function getChartJs() {

    var counts = document.getElementById("line_chart").getAttribute("data-counts");
    counts = counts.substring(1,counts.length-1).replace(/[\\']/g, "").split(', ');

    for (var i = 0; i < counts.length; i++) {
        counts[i] = parseFloat(counts[i])
    };

    var config = {
        type: 'line',
        data: {
            labels: ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sabado"],
            datasets: [{
                label: "Quantidade Abertos (%)",
                data: counts,
                borderColor: 'rgba(0, 188, 212, 0.75)',
                backgroundColor: 'rgba(0, 188, 212, 0.3)',
                pointBorderColor: 'rgba(0, 188, 212, 0)',
                pointBackgroundColor: 'rgba(0, 188, 212, 0.9)',
                pointBorderWidth: 1
            }]
        },
        options: {
            responsive: true,
            legend: false
        }
    }
    return config;
}