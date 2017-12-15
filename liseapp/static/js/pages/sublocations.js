


$(function () {
    new Chart(document.getElementById("pie_chart_sub").getContext("2d"), getChartPieJs());
});

function getChartPieJs() {
    console.log('ok')

    var sublocation = document.getElementById("pie_chart_sub").getAttribute("data-sublocation");
    sublocation = sublocation.substring(1,sublocation.length-1).replace(/[\\']/g, "").split(', ');

    var counts = document.getElementById("pie_chart_sub").getAttribute("data-count");
    counts = counts.substring(1,counts.length-1).replace(/[\\']/g, "").split(', ');


    var colors = [
        "rgb(233, 30, 99)",
        "rgb(255, 193, 7)",
        "rgb(0, 188, 212)",
        "rgb(139, 195, 74)",
        'rgb(255, 152, 0)', 
        'rgb(0, 150, 136)', 
        'rgb(96, 125, 139)',
    ]
    var vezes = parseInt(sublocation.length/colors.length)+1
    var list_colors = []

    for (var i = 0; i < vezes; i++) {
        list_colors = list_colors.concat(colors)
    };



    var config = {
        type: 'pie',
        data: {
            datasets: [{
                data: counts,
                backgroundColor: list_colors,
            }],
            labels: sublocation
        },
        options: {
            responsive: true,
            legend: sublocation
        }
    }
    return config;
}