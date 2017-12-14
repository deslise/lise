$(function () {

    //Widgets count
    $('.count-to').countTo();


    //Sales count to
    $('.sales-count-to').countTo({
        formatter: function (value, options) {
            return '$' + value.toFixed(2).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, ' ').replace('.', ',');
        }
    });

    initDonutChartAll();
});

var realtime = 'on';
function initDonutChartAll() {

    var topics = document.getElementById("donut_chart_all").getAttribute("data-topics");
    topics = topics.substring(1,topics.length-1).replace(/[\\']/g, "").split(', ');
    var counts = document.getElementById("donut_chart_all").getAttribute("data-counts");
    // alert((1.9887).toFixed(2));
    counts = counts.substring(1,counts.length-1).split(', ');
    var soma = 0;
    for (var i = 0; i < counts.length; i++) {
        soma += parseInt(counts[i])
    };
    var data = new Array();
    var soma_p = 0.0
    for (var i = 0; i < counts.length; i++) {
        val = parseFloat((parseInt(counts[i])/soma * 100).toFixed(2)) 
        console.log(val);
        data[i] = {
            label: topics[i],
            value: val
        }
        soma_p += val
    };    
    data[counts.length] = {
        label: 'Sem Categoria',
        value: parseFloat((soma_p/soma * 100).toFixed(2))
    };

    Morris.Donut({
        element: "donut_chart_all",
        data: data,
        colors: ['rgb(233, 30, 99)', 'rgb(0, 188, 212)', 'rgb(255, 152, 0)', 'rgb(0, 150, 136)', 'rgb(96, 125, 139)'],
        formatter: function (y) {
            return y + '%'
        }
    });
}