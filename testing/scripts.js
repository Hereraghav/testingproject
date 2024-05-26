$(document).ready(function() {
    $('#uploadForm').on('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if (response.success) {
                    $('#progress').text(response.success);
                    loadTable(response.filename);
                } else {
                    $('#progress').text(response.error);
                }
            }
        });
    });

    function loadTable(filename) {
        $.get('/data/' + filename, function(data) {
            $('#data-table').html(data);
            $('table').DataTable();
        });
    }
});
function loadTable(filename) {
    $.get('/data/' + filename, function(data) {
        $('#data-table').html(data);
        $('table').DataTable();
    });

    $('#calculatePricing').on('click', function() {
        $.get('/calculate-pricing/' + filename, function(data) {
            $('#data-table').html(data);
            $('table').DataTable();
        });
    });
}
