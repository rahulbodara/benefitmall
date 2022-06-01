$(function () {
	/*
	Instantiate empty translatables object
	Object will be formatted like the following:
		{
			'en':
				[
					field_object_1,
					field_object_2,
					...
				]
			,
		}
	*/
	var translatables = {};

	// Function when language is changed
	function change_language(active_language) {
	    
	    // Toggle language fields
	    for (var key in translatables) {
	        translatables[key].map( function(obj) {
	            obj.toggle(key === active_language)
			});
	    }

	    // Change label text in tabs to active language abbreviation
	    $("ul[class='tab-nav merged'] li a").each(function() {
	        var tab_label = $.trim($(this).text());
	        var tab_lang = tab_label.lastIndexOf(' ');
	        var tab_label_root = tab_lang >= 0 ? tab_label.substr(0, tab_lang) : tab_label;                
	        $(this).html(tab_label_root + ' [' + $('#language_select').val() + ']');
	    });
	}

	// Onload populate translatables object
    $('ul[class="objects"]').find('label:contains(" [")').each(function () {
        var label = $.trim($(this).text());
        var language = label.substr(label.lastIndexOf('[') + 1, 2);
        if (!(language in translatables)) {
            translatables[language] = [];
        }
        translatables[language].push($(this).closest('li'));
    });

    // Create language select
    var s = $('<select class="choice_field" id="language_select" style="padding:20px; width: auto; height:30px; margin:6px; -webkit-appearance:menulist; -moz-appearance:menulist; appearance:menulist;" />');
    
    // Create and append language options to lanaguage select
    for (var key in translatables) {
        $('<option />', {value: key, text: langs_obj[key]}).appendTo(s);
    }

    // Insert language select into DOM
    $("ul[class='tab-nav merged']").append(s);
    
    // Listener call to change function
    $("#language_select").on('change', function () {
        change_language(this.value);
    });

    // Manual call to change function
    change_language("en");
});