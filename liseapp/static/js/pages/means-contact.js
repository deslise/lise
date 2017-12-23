


$(function () {
    if (document.getElementById("bar_vert")){
        new Chart(document.getElementById("bar_vert").getContext("2d"), getBarVertJs());
    };
    if (document.getElementById("bar_vert_mixture")){
        new Chart(document.getElementById("bar_vert_mixture").getContext("2d"), getBarVertMixtureJs());
    };
});

function getBarVertJs() {
    console.log('ok')

    var phone = document.getElementById("bar_vert").getAttribute("data-phone");
    phone = parseFloat(phone.replace(',', "."))

    var site = document.getElementById("bar_vert").getAttribute("data-site");
    site = parseFloat(site.replace(',', "."))

    var face = document.getElementById("bar_vert").getAttribute("data-face");
    face = parseFloat(face.replace(',', "."))

    // console.log(phone, site, face)


    var config = {
        type: 'horizontalBar',
        data: {
            labels: ["Telefone", "Website", "Fanpage"],
            datasets: [{
                label: "Usadas pelos concorrentes (%)",
                data: [phone, site, face],
                backgroundColor: ["rgb(233, 30, 99)",
                                    "rgb(255, 193, 7)",
                                    "rgb(0, 188, 212)"]
            }]
        },
        options: {
            responsive: true,
            legend: false,
            barPercentage: 1.0,
        }
    }
    return config;
}

function getBarVertMixtureJs() {
    console.log('ok')

    var mixture = document.getElementById("bar_vert_mixture").getAttribute("data-mixture");
    mixture = mixture.substring(1,mixture.length-1).replace(/[\\']/g, "").split(', ');

    // for (var i = 0; i < mistake.legend; i++) {
    //     phone = parseFloat(phone.replace(',', "."))
    // };

    // console.log(phone, site, face)

    console.log(mixture)

    var config = {
        type: 'horizontalBar',
        data: {
            labels: ["Somente Telefone", "Somente Website", "Somente Fanpage", 'Telefone e Website', 'Telefone e Fanpage', 'Website e Fanpage', 'Telefone, Website e Fanpage', 'Nenhum desses'],
            datasets: [{
                label: "Usadas pelos concorrentes (%)",
                data: mixture,
                backgroundColor: ["rgb(233, 30, 99)",
                                "rgb(255, 193, 7)",
                                "rgb(0, 188, 212)",
                                pattern.draw('diagonal-right-left', 'rgb(233, 30, 99)'),
                                pattern.draw('diagonal-right-left', 'rgb(255, 193, 7)'),
                                pattern.draw('diagonal-right-left', 'rgb(0, 188, 212)'),
                                pattern.draw('zigzag-vertical', 'rgb(233, 30, 99)'),
                                pattern.draw('zigzag-vertical', 'rgb(255, 193, 7)')]
            }]
        },
        options: {
            responsive: true,
            legend: false,
            barPercentage: 1.0

        }
    }
    return config;
}