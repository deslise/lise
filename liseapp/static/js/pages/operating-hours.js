
$(function () {
	new Chart(document.getElementById("line_chart").getContext("2d"), getChartJs());

});
function getChartJs() {
	console.log('ok')

	var open = document.getElementById("line_chart").getAttribute("data-open");
	console.log('open:',open)
	var close = document.getElementById("line_chart").getAttribute("data-close");
	console.log('close:',close)

	var config = {
            type: 'line',
            data: {
                labels: ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sabado"],
                datasets: [{
                    label: "My First dataset",
                    data: ['00', '08', '08:30', '08', '08', '08', '00'],
                    borderColor: 'rgba(0, 188, 212, 0.75)',
                    backgroundColor: 'rgba(0, 188, 212, 0.3)',
                    pointBorderColor: 'rgba(0, 188, 212, 0)',
                    pointBackgroundColor: 'rgba(0, 188, 212, 0.9)',
                    pointBorderWidth: 1
                }, {
                        label: "My Second dataset",
                        data: ['00', '18', '18', '18', '18', '18', '00'],
                        borderColor: 'rgba(233, 30, 99, 0.75)',
                        backgroundColor: 'rgba(233, 30, 99, 0.3)',
                        pointBorderColor: 'rgba(233, 30, 99, 0)',
                        pointBackgroundColor: 'rgba(233, 30, 99, 0.9)',
                        pointBorderWidth: 1
                    }]
            },
            options: {
                responsive: true,
                legend: false
            }
        }
    return config
}