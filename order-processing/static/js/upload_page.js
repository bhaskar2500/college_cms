$(document).ready(function() {
    var bar = $('.bar');
    var percent = $('.percent');
    var status = $('#status');

    $('.uploadform').ajaxForm({
        beforeSend: function() {
            status.empty();
            var percentVal = '0%';
            bar.width(percentVal)
            percent.html(percentVal);
        },
        uploadProgress: function(event, position, total, percentComplete) {
            var percentVal = percentComplete + '%';
            bar.width(percentVal)
            percent.html(percentVal);
            //console.log(percentVal, position, total);
        },
        success: function(data) {
            var percentVal = '100%';
            bar.width(percentVal)
            percent.html(percentVal);
            data = JSON.parse(data);
            process_file(data.data);
        },
            complete: function(xhr) {
            status.html(xhr.responseText);
        }
    });
});

function process_file(params) {
    $.post('/admin/process', params, function(data) {
      console.log(JSON.parse(data));
    });
}
