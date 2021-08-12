// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

//service section owl carousel
$(".service_owl-carousel").owlCarousel({
    autoplay: true,
    center: true,
    nav: true,
    loop: true,
    margin: 0,
    responsive: {
        0: {
            items: 1
        },
        768: {
            items: 3,
        },
        991: {
            items: 3
        }
    }
});

// nice select
$(document).ready(function () {
    $('select').niceSelect();
});

// number increse animation
$('.count').each(function () {
    $(this).prop('Counter', 0).animate({
        Counter: $(this).text()
    }, {
        duration: 4000,
        easing: 'swing',
        step: function (now) {
            $(this).text(Math.ceil(now));
        }
    });
});