function GoogleCalendarEditBlock(runtime, element) {
    $('.save-button', element).bind('click', function() {
        var data = {
            'display_name': $('.edit-display-name', element).val(),
            'calendar_id': $('.edit-calendar-id', element).val(),
            'default_view': $('select.edit-label_type > option:selected', element).val(),
        };

        $('.xblock-editor-error-message', element).html();
        $('.xblock-editor-error-message', element).css('display', 'none');
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                window.location.reload(false);
            } else {
                $('.xblock-editor-error-message', element).html('Error: '+response.message);
                $('.xblock-editor-error-message', element).css('display', 'block');
            }
        });
    });

    $('.cancel-button', element).bind('click', function() {
        runtime.notify('cancel', {});
    });
}
