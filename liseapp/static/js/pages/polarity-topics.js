
$(function () {
    new Chart(document.getElementById("bar_chart_all").getContext("2d"), getChartJsAll());
});

function getChartJsAll() {
     var pos = document.getElementById("bar_chart_all").getAttribute("data-pos");
     var neg = document.getElementById("bar_chart_all").getAttribute("data-neg");
     var neu = document.getElementById("bar_chart_all").getAttribute("data-neu");
     var counts = document.getElementById("bar_chart_all").getAttribute("data-count");
     var topics = document.getElementById("bar_chart_all").getAttribute("data-topics");
     topics = topics.substring(1,topics.length-1).replace(/[\\']/g, "").split(', ');
     pos = pos.substring(1,pos.length-1).split(', '); 
     neg = neg.substring(1,neg.length-1).split(', '); 
     neu = neu.substring(1,neu.length-1).split(', '); 
     counts = counts.substring(1,counts.length-1).split(', ');
     var data_pos = new Array();
     var data_neg = new Array();
     var data_neu = new Array();
     var data_topics = new Array();
     for (var i = 0; i < counts.length; i++) {
        data_pos[i] = parseFloat((parseInt(pos[i])/parseInt(counts[i]) * 100).toFixed(2)) 
        data_neg[i] = parseFloat((parseInt(neg[i])/parseInt(counts[i]) * 100).toFixed(2)) 
        data_neu[i] = parseFloat((parseInt(neu[i])/parseInt(counts[i]) * 100).toFixed(2)) 
        data_topics[i] = topics[i]
    };

    var config = {
        type: 'bar',
        data: {
            labels: data_topics,
            datasets: [{
                label: "Positivo (%)",
                data: data_pos,
                backgroundColor: 'rgba(0, 188, 212, 0.8)'
            }, 
            {
                label: "Negativo (%)",
                data: data_neg,
                backgroundColor: 'rgba(233, 30, 99, 0.8)'
            },
            {
                label: "Neutro (%)",
                data: data_neu,
                backgroundColor: 'rgb(255, 152, 0, 0.8)'
            }]
        },
        options: {
            responsive: true,
            legend: false
        }
    }
    return config;
}