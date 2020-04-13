$(function () {
    /**************************************************************************************************/
    // Page title container selector
    var header_div = $('div.left.col9.header-title');
    /**************************************************************************************************/


    /**************************************************************************************************/
    // Add 'Show in Explorer View' button to edit pages
    var explorer_button = document.createElement('a');
    explorer_button.innerHTML = 'Show in Explorer';
    explorer_button.href = window.location.href.replace('/edit/', '/');
    explorer_button.classList.add('button', 'button-small', 'icon', 'icon-folder-open-inverse');
    header_div.append(explorer_button);
    /**************************************************************************************************/


    /**************************************************************************************************/
    // Toggler for LinkBlock type selector
    function linkBlockToggler(elem){
        var value = $(elem).find('input:checked').val();
        var container = $(elem).closest('.link-block');

        // Loop through link items and toggle display and class
        if (value === '') {
            var items = ['url', 'page', 'document', 'email', 'phone', 'link_text', 'link_format'];
            $.each(items, function(index, item) {
                container.find('.fieldname-'+item).parent().closest('.field').hide().removeClass('required');
            }.bind(this));
        } else {
            var items = ['url', 'page', 'document', 'email', 'phone'];
            $.each(items, function(index, item) {
                container.find('.fieldname-'+item).parent().closest('.field').hide().removeClass('required');
            }.bind(this));
            var items = [value, 'link_text'];
            $.each(items, function(index, item) {
                container.find('.fieldname-'+item).parent().closest('.field').show().addClass('required');
            }.bind(this));
            container.find('.fieldname-link_format').parent().closest('.field').show();
        }

    }

    // linkBlockToggler call on change
    $('body').on('change', '.link-block .fieldname-link_type', function() {
       linkBlockToggler(this);
    });
    /**************************************************************************************************/


    /**************************************************************************************************/
    // Toggler for MediaBlock mode selector
    function mediaBlockToggler(elem){
        var value = $(elem).find('input:checked').val();
        var container = $(elem).closest('.media-block');

        // Select media items and toggle display and class
        if (value === 'image-video') {
            container.find('.fieldname-video_source').parent().closest('.field').show();
            container.find('.fieldname-video_id').parent().closest('.field').show().addClass('required');
        } else {
            container.find('.fieldname-video_source').parent().closest('.field').hide();
            container.find('.fieldname-video_id').parent().closest('.field').hide().removeClass('required');
        }

    }

    // mediaBlockToggler call on change
    $('body').on('change', '.media-block .fieldname-mode', function() {
       mediaBlockToggler(this);
    });
    /**************************************************************************************************/


    /**************************************************************************************************/
    // Toggler for BackgroundBlock mode selector
    function backgroundBlockToggler(elem){
        var value = $(elem).find('input:checked').val();
        var container = $(elem).closest('.background-block');

        // Loop through mode items and toggle display and class
        var items = ['background_image', 'image_effect', 'image_invert', 'image_overlay'];
        if (value === 'imagebg') {
            $.each(items, function(index, item) {
                container.find('.fieldname-'+item).parent().closest('.field').show();
            }.bind(this));
            container.find('.fieldname-image').parent().closest('.field').addClass('required');
        } else {
            $.each(items, function(index, item) {
                container.find('.fieldname-'+item).parent().closest('.field').hide();
            }.bind(this));
            container.find('.fieldname-image').parent().closest('.field').removeClass('required');
        }
    }

    // backgroundBlockToggler call on change
    $('body').on('change', '.background-block .fieldname-mode', function() {
       backgroundBlockToggler(this);
    });
    /**************************************************************************************************/


    /**************************************************************************************************/
    // Toggler for BackgroundBlock mode selector
    function backgroundBlockSizeToggler(elem){
        var value = $(elem).find('input:checked').val();
        var container = $(elem).closest('.background-block');

        if(value == 'padding'){
            container.find('.fieldname-padding').parent().closest('.field').show();
            container.find('.fieldname-sizing').parent().closest('.field').hide();
        } else {
            container.find('.fieldname-padding').parent().closest('.field').hide();
            container.find('.fieldname-sizing').parent().closest('.field').show();
        }
    }

    // backgroundBlockToggler call on change
    $('body').on('change', '.background-block .fieldname-sizing_mode', function() {
       backgroundBlockSizeToggler(this);
    });
    /**************************************************************************************************/


    // /**************************************************************************************************/
    // // Toggler for Blog video source selector
    // function videoSourceToggler(elem){
    //     var value = $(elem).find('input:checked').val();
    //     var container = $(elem).closest('ul.fields');
    //
    //     // Toggle items
    //     if (value === '') {
    //         container.find('#id_video_id').closest('li').hide().removeClass('required');
    //     } else {
    //         container.find('#id_video_id').closest('li').show().addClass('required');
    //     }
    // }
    //
    // // videoSourceToggler call on load
    // videoSourceToggler($('#id_video_source'));
    //
    // // videoSourceToggler call on change
    // $('body').on('change', '#id_video_source', function() {
    //    videoSourceToggler(this);
    // });
    // /**************************************************************************************************/


    /**************************************************************************************************/
    // Toggler for ProcessBlock mode selector
    function processBlockToggler(elem){
        var value = $(elem).find('input:checked').val();
        var container = $(elem).closest('.process-block');

        // Select media items and toggle display and class
        if (value === 'media') {
            container.find('.fieldname-process_orientation').parent().closest('.field').show();
            container.find('.media-block').parent().closest('.field').show();
            container.find('.media-block .fieldname-image').parent().closest('.field').show().addClass('required');
        } else {
            container.find('.fieldname-process_orientation').parent().closest('.field').hide();
            container.find('.media-block').parent().closest('.field').hide();
            container.find('.media-block .fieldname-image').parent().closest('.field').hide().removeClass('required');
        }

    }

    // processBlockToggler call on change
    $('body').on('change', '.process-block .fieldname-process_layout', function() {
       processBlockToggler(this);
    });
    /**************************************************************************************************/


    /**************************************************************************************************/
     function galleryBlockToggler(elem){
        var value = $(elem).find('input:checked').val();
        var container = $(elem).closest('.gallery-block');

        if (value === 'overlaytext') {
            container.find('.fieldname-hover').parent().closest('.field').show();
        } else {
            container.find('.fieldname-hover').parent().closest('.field').hide();
        }

    }

    $('body').on('change', '.gallery-block .fieldname-mode', function() {
       galleryBlockToggler(this);
    });
    /**************************************************************************************************/

    /**************************************************************************************************/
     function ctaBlockToggler(elem){
        var value = $(elem).find('input:checked').val();
        var container = $(elem).closest('.cta-block');

        if (value === 'horizontal') {
            container.find('.fieldname-page').parent().closest('.field').hide();
            // container.find('.fieldname-subhead_size').parent().closest('.field').show();
            container.find('.fieldname-body').parent().closest('.field').show();
            container.find('.fieldname-body').parent().closest('.field').addClass('required');
            container.find('.link-block').closest('.field').show();
            container.find('.fieldname-body_size').parent().closest('.field').show();
            container.find('.fieldname-outline').parent().closest('.field').show();
        } else {
            container.find('.fieldname-page').parent().closest('.field').show();
            // container.find('.fieldname-subhead_size').parent().closest('.field').hide();
            container.find('.fieldname-body').parent().closest('.field').hide();
            container.find('.fieldname-body').parent().closest('.field').removeClass('required');
            container.find('.link-block').closest('.field').hide();
            container.find('.fieldname-body_size').parent().closest('.field').hide();
            container.find('.fieldname-outline').parent().closest('.field').hide();
        }

    }

    $('body').on('change', '.cta-block .fieldname-layout', function() {
       ctaBlockToggler(this);
    });
    /**************************************************************************************************/

    /**************************************************************************************************/
     function titleBlockToggler(elem){
        var value = $(elem).find('input:checked').val();
        var container = $(elem).closest('.title-block');

        if (value === 'fixed') {
            container.find('.fieldname-switchable').parent().closest('.field').show();

        } else {
            container.find('.fieldname-switchable').parent().closest('.field').hide();

        }

    }

    $('body').on('change', '.title-block .fieldname-layout', function() {
       titleBlockToggler(this);
    });
    /**************************************************************************************************/



    /**************************************************************************************************/
     function pricingBlockToggler(elem){
        var value = $(elem).find('input:checked').val();
        var container = $(elem).closest('.pricing-block');

        if (value === 'feature_2') {
            container.find('[id*="features-list"]').closest('.field').hide();
            container.find('.testimonial-block').closest('.field').hide();
        } else if (value === 'feature_3')
        {
            container.find('[id*="features-list"]').closest('.field').show();
            container.find('.testimonial-block').closest('.field').hide();
        }
        else{
            container.find('[id*="features-list"]').closest('.field').hide();
            container.find('.testimonial-block').closest('.field').show();
        }

    }

    $('body').on('change', '.pricing-block .fieldname-layout', function() {
       pricingBlockToggler(this);
    });
    /**************************************************************************************************/


    /**************************************************************************************************/
     function mediaTitleBlockToggler(elem){
        var value = $(elem).find('input:checked').val();
        var container = $(elem).closest('.media-title-block');

        if (value === 'three_column') {
            container.find('.fieldname-small_image').parent().closest('.field').show();
            container.find('.fieldname-small_image').parent().closest('.field').addClass('required');
            container.find('.fieldname-switchable').parent().closest('.field').hide();
            container.find('.fieldname-vertical_alignment').parent().closest('.field').hide();
        }
        else{
            container.find('.fieldname-small_image').parent().closest('.field').hide();
            container.find('.fieldname-small_image').parent().closest('.field').removeClass('required');
            container.find('.fieldname-switchable').parent().closest('.field').show();
            container.find('.fieldname-vertical_alignment').parent().closest('.field').show();
        }

    }

    $('body').on('change', '.media-title-block .fieldname-layout', function() {
       mediaTitleBlockToggler(this);
    });
    /**************************************************************************************************/


    /**************************************************************************************************/
    // General function called from observer
    var observer = new MutationObserver(function(mutations) {
        // linkBlockToggler call on observed mutation
        $('.link-block .fieldname-link_type').each(function() {
           linkBlockToggler(this);
        });

        // mediaBlockToggler call on observed mutation
        $('.media-block .fieldname-mode').each(function() {
           mediaBlockToggler(this);
        });

        // backgroundBlockToggler call on observed mutation
        $('.background-block .fieldname-mode').each(function() {
           backgroundBlockToggler(this);
        });

        // backgroundBlockSizeToggler call on observed mutation
        $('.background-block .fieldname-sizing_mode').each(function() {
           backgroundBlockSizeToggler(this);
        });

        // processBlockToggler call on observed mutation
        $('.process-block .fieldname-process_layout').each(function() {
           processBlockToggler(this);
        });

        // galleryBlockToggler call on observed mutation
        $('.gallery-block .fieldname-mode').each(function() {
           galleryBlockToggler(this);
        });

        // pricingBlockToggler call on observed mutation
        $('.pricing-block .fieldname-layout').each(function() {
           pricingBlockToggler(this);
        });
        // ctaBlockToggler call on observed mutation
        $('.cta-block .fieldname-layout').each(function() {
           ctaBlockToggler(this);
        });
        // titleBlockToggler call on observed mutation
        $('.title-block .fieldname-layout').each(function() {
           titleBlockToggler(this);
        });
        // imageFreatureBlockToggler call on observed mutation
        $('.image-feature-block .fieldname-layout').each(function() {
           imageFeatureBlockToggler(this);
        });
        // mediaTitleBlockToggler call on observed mutation
        $('.media-title-block .fieldname-layout').each(function() {
           mediaTitleBlockToggler(this);
        });



    });

    // General listener for added/removed nodes on body
    observer.observe(document.body, {
        childList: true,
        subtree: true,
    });
    /**************************************************************************************************/



});