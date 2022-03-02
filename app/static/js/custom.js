$(function () {
    /**************************************************************************************************/
    // Popup window for social sharing
    $('.popup').click(function(e){
        e.preventDefault();
        var href = $(this).attr('href');
        var left = ($(window).width() / 2) - (580 / 2);
        var top = ($(window).height() / 2) - (500 / 2);
        window.open(href, 'popup', 'width=580, height=500, top='+top+', left='+left);
    });
    /**************************************************************************************************/

    // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
    $(document).ready(function() {
        var stickyBottom = $('.navigation').offset().top + $('.navigation').height();

        $(window).scroll(function() {
            var windowTop = $(window).scrollTop();
            console.log(stickyBottom)
            if (stickyBottom < windowTop) {
                $(".nav-placeholder").height($(".navigation").outerHeight());
                $('.navigation').css('position', 'fixed').css('top', '0');
            } else {
                $(".nav-placeholder").height(0);
                $('.navigation').css('position', 'relative').css('top', 'unset');
            }
        });
    });

    /**************************************************************************************************/
    // Image caption insert
    $('.article__body .rich-text img').each(function(index, item){
        var alt = $(item).attr('alt');

        var image = $(item).removeAttr('width').removeAttr('height').prop('outerHTML');
        var classes = $(item).attr('class');
        if (classes.indexOf('left') !== -1) {
            classes = 'float-left pull-left'
        } else if (classes.indexOf('right') !== -1) {
            classes = 'float-right pull-right'
        }
        $(item).replaceWith('<figure class="'+classes+'">'+image+'<figcaption>'+alt+'</figcaption></figure>');
    });
    /**************************************************************************************************/


    /**************************************************************************************************/
    // Set focus to search box
    var search_box = $('.notification.search-box');
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === "class") {
                $('input[name="q"]').focus()
            }
        });
    });
    observer.observe(search_box[0], {
        attributes: true
    });

    // Handle search submit
    $('input[name="q"]').keypress(function (e) {
        if (e.which == 13) {
            window.location.href = '/search/?q=' + this.value;
            return false;
        }
    });
    /**************************************************************************************************/
});