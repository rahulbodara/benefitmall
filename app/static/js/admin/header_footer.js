$(function () {

    /**************************************************************************************************/
    // Toggler for Navigation Type selector
    function navTypeToggler(elem){
        // console.log(elem.val())
        var container = $(elem).closest('ul.fields');
        var show_list = [];
        var hide_list = [];
        switch(elem.val()){
            default:
            case('no-nav.html'):
                show_list = [];
                hide_list = [
                    'id_header_automatic_nav',
                    'header_links-list',
                    'header_buttons-list',
                    'id_header_banner_text_1',
                    'id_header_banner_text_2',
                ];
                break;
            case('standard-bar.html'):
            case('centered-bar.html'):
            case('app-bar.html'):
                show_list = [
                    'id_header_automatic_nav',
                    'header_buttons-list',
                ];
                hide_list = [
                    'id_header_banner_text_1',
                    'id_header_banner_text_2',
                ];
                break;
            case('side-bar.html'):
                show_list = [
                    'id_header_automatic_nav',
                ];
                hide_list = [
                    'header_buttons-list',
                    'id_header_banner_text_1',
                    'id_header_banner_text_2',
                ];
                break;
            case('full-screen.html'):
                show_list = [
                    'id_header_automatic_nav',
                    'id_header_banner_text_1',
                    'id_header_banner_text_2',
                ];
                hide_list = [
                    'header_buttons-list',
                ];
                break;
        }

        $.each(show_list, function (index, item) {
            container.find('#' + item).closest('li').show().addClass('required');
            if(item=='id_header_automatic_nav'){
                autoNavToggler($('#id_header_automatic_nav'));
            }
        }.bind(this));

        $.each(hide_list, function(index, item) {
            container.find('#'+item).closest('li').hide().removeClass('required');
        }.bind(this));

    }

    // navTypeToggler call on load
    navTypeToggler($('#id_navigation_type'));
    // navTypeToggler call on change
    $('body').on('change', '#id_navigation_type', function() {
       navTypeToggler($(this));
    });
    /**************************************************************************************************/

    /**************************************************************************************************/
    // Toggler for Footer Type selector
    function footerTypeToggler(elem){
        // console.log(elem.val())
        var container = $(elem).closest('ul.fields');
        var show_list = [];
        var hide_list = [];
        switch(elem.val()) {
            default:
            case('no-footer.html'):
            case('short-5.html'):
                // Hide list
                hide_list = [
                    'footer_links-list',
                    'footer_buttons-list',
                    'footer_utility_links-list',
                    'footer_category_links-list',
                ];

                break;
            case('long-1.html'):
                // Show list
                show_list = [
                    'footer_utility_links-list',
                    'footer_category_links-list',
                ];

                // Hide list
                hide_list = [
                    'footer_links-list',
                    'footer_buttons-list',
                ];

                break;
            case('long-2.html'):
                // Show list
                show_list = [
                    'footer_category_links-list',
                ];

                // Hide list list
                hide_list = [
                    'footer_links-list',
                    'footer_buttons-list',
                    'footer_utility_links-list',
                ];

                break;
            case('short-2.html'):
                // Show list
                show_list = [
                    'footer_links-list',
                    'footer_buttons-list',
                    'footer_utility_links-list',
                ];

                // Hide list
                hide_list = [
                    'footer_category_links-list',
                ];

                break;
            case('short-1.html'):
            case('short-3.html'):
                // Show list
                show_list = [
                    'footer_links-list',
                    'footer_utility_links-list',
                ];

                // Hide list
                hide_list = [
                    'footer_buttons-list',
                    'footer_category_links-list',
                ];

                break;
            case('short-4.html'):
            case('subscribe.html'):
                // Show list
                show_list = [
                    'footer_links-list',
                ];

                // Hide list
                hide_list = [
                    'footer_buttons-list',
                    'footer_utility_links-list',
                    'footer_category_links-list',
                ];

                break;
        }

        $.each(show_list, function (index, item) {
            container.find('#' + item).closest('li').show().addClass('required');
        }.bind(this));

        $.each(hide_list, function (index, item) {
            container.find('#' + item).closest('li').hide().removeClass('required');
        }.bind(this));

    }

    // footerTypeToggler call on load
    footerTypeToggler($('#id_footer_type'));
    // footerTypeToggler call on change
    $('body').on('change', '#id_footer_type', function() {
       footerTypeToggler($(this));
    });
    /**************************************************************************************************/

    /**************************************************************************************************/
    // Toggler for Utility Nav selector
    function utilityNavToggler(elem){
        var value = elem.is(':checked');
        var container = $(elem).closest('ul.fields');

        // Loop through link items and toggle display and class
        if (value) {
            var items = ['id_utility_switched', 'id_utility_background_color','id_utility_text', 'utility_links-list'];
            $.each(items, function(index, item) {
                container.find('#'+item).closest('li').show()
            }.bind(this));
        } else {
            var items = [value, 'id_utility_switched', 'id_utility_background_color', 'id_utility_text', 'utility_links-list'];
            $.each(items, function(index, item) {
                container.find('#'+item).closest('li').hide()
            }.bind(this));
        }

    }

    // utilityNavToggler call on load
    utilityNavToggler($('#id_header_utility_nav'));
    // autoNavToggler call on change
    $('body').on('change', '#id_header_utility_nav', function() {
       utilityNavToggler($(this));
    });
    /**************************************************************************************************/

    /**************************************************************************************************/
    // Toggler for Auto Nav selector
    function autoNavToggler(elem){
        var value = elem.is(':checked');
        var container = $(elem).closest('ul.fields');

        // Loop through link items and toggle display and class
        if (value) {
            var items = ['header_links-list',];
            $.each(items, function(index, item) {
                container.find('#'+item).closest('li').hide().removeClass('required');
            }.bind(this));
        } else {
            // Hide these items
            var items = ['header_links-list'];
            $.each(items, function(index, item) {
                container.find('#'+item).closest('li').hide().removeClass('required');
            }.bind(this));
            // Show these items
            var items = [value, 'header_links-list', 'header_buttons-list',];
            $.each(items, function(index, item) {
                container.find('#'+item).closest('li').show().addClass('required');
            }.bind(this));
            // container.find('.fieldname-link_format').closest('li').show();
        }

    }

    // autoNavToggler call on load
    autoNavToggler($('#id_header_automatic_nav'));
    // autoNavToggler call on change
    $('body').on('change', '#id_header_automatic_nav', function() {
       autoNavToggler($(this));
    });
    /**************************************************************************************************/


    /**************************************************************************************************/
    // General function called from observer
    var observer = new MutationObserver(function(mutations) {
        // autoNavToggler call on observed mutation
        $('#id_header_automatic_nav').each(function() {
           autoNavToggler($(this));
        });
        $('#id_navigation_type').each(function() {
           navTypeToggler($(this));
        });
        $('#id_footer_type').each(function() {
           footerTypeToggler($(this));
        });
        $('#id_header_utility_nav').each(function() {
           utilityNavToggler($(this));
        });
    });

    // General listener for added/removed nodes on body
    observer.observe(document.body, {
        childList: true,
        subtree: true,
    });
    /**************************************************************************************************/

});