//jquery-click-scroll
//by syamsul'isul' Arifin

var sectionArray = [1, 2, 3, 4, 5];

$.each(sectionArray, function (index, value) {

    $(document).scroll(function () {
        // var offsetSection = $('#' + 'section_' + value).offset().top - 90;
        var section = $('#' + 'section_' + value);
        if (section.length > 0) {
            var offsetSection = section.offset().top - 90;
        }
        var docScroll = $(document).scrollTop();
        var docScroll1 = docScroll + 1;


        if (docScroll1 >= offsetSection) {
            $('.navbar-nav .nav-item .nav-link').removeClass('active');
            $('.navbar-nav .nav-item .nav-link:link').addClass('inactive');
            $('.navbar-nav .nav-item .nav-link').eq(index).addClass('active');
            $('.navbar-nav .nav-item .nav-link').eq(index).removeClass('inactive');
        }

    });

    $('.click-scroll').eq(index).click(function (e) {
        var offsetClick = $('#' + 'section_' + value).offset().top - 90;
        e.preventDefault();
        $('html, body').animate({
            'scrollTop': offsetClick
        }, 300)
    });

});

