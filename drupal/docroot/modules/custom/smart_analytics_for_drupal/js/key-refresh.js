(function (Drupal, $, once) {

  /**
   * .Refreshes the key select options after closing the key creation dialog.
   *
   * @param {object} context
   *  Drupal behaviors context.
   */
  Drupal.behaviors.smartAnalyticsKeyRefresh = {
    attach: function (context) {
      $(once('key-refresh', 'body', context)).on('dialog:afterclose', function (event, dialog, $element) {
        // Reloads the key select options via AJAX.
        const $select = $('select[name="key_reference"]');
        if ($select.length) {
          $.ajax({
            url: Drupal.url('smart-analytics/refresh-keys'),
            type: 'GET',
            dataType: 'json',
            success: function (data) {
              if (data.options) {
                $select.empty();
                $.each(data.options, function (val, label) {
                  $select.append($('<option></option>').attr('value', val).text(label));
                });
                // Select automatically the last created key.
                if (data.last_created) {
                  $select.val(data.last_created);
                }
              }
            }
          });
        }
      });
    }
  };
})(Drupal, jQuery, once);
