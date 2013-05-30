/* = FILE UPLOAD ============================================================== */
!function ($) {
    "use strict"; // jshint ;_;

    var filesel = $('input[id=filesel]');
    filesel.change(function() {
        $('#filename').val($(this).val());
    });
    filesel.css( 'position', 'absolute' );
    filesel.css( 'visibility', 'hidden' );

    $('#filealert').css( 'visibility', 'hidden' );

    $('#filebrowse').click(function() {
        $('#filesel').click();
    });

    $('#filesend').click(function() {
        $('#filebar > .bar').replaceWith('<div id="filebar" class="bar" style="width: 0%;"></div>');
        $('#filealert').css( 'visibility', 'hidden' );
        $('#filebar').addClass('progress-striped');
        $('#filebar').addClass('active');
        var xhr = new XMLHttpRequest();
        if ( xhr.upload ) {
            xhr.upload.onprogress = function(e) {
                var done = e.position || e.loaded, total = e.totalSize || e.total;
                var perc = (Math.floor(done/total*1000)/10);
                $('#filebar > .bar').css('width', '' + perc + '%' );
            };
        }
        xhr.onreadystatechange = function(e) {
            if ( 4 == this.readyState ) {
                $('#filealert').css( 'visibility', 'visible' );
                $('#filebar > .bar').css('width', '100%' );
                $('#fileform').css( 'visibility', 'visible');
                $('#filebar').removeClass('progress-striped');
                $('#filebar').removeClass('active')
            }
        };

        xhr.open( 'PUT', '/upload', true );

        var form = $('#fileform')[0];
        var fd = new FormData( form );
        xhr.send( fd );

        $('#fileform').css( 'visibility', 'hidden');
    });

}(window.jQuery);
