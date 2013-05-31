/* = FILE UPLOAD ============================================================== */
!function ($) {
    "use strict"; // jshint ;_;

    var filesel = $('input[id=filesel]');
    filesel.change( function(){
        $('#filename').val( $(this).val() );
    });
    filesel.css( 'position', 'absolute' );
    filesel.css( 'visibility', 'hidden' );

    $('#filealert').css( 'visibility', 'hidden' );

    $('#filebrowse').click( function(){
        $('#filesel').click();
    });

    $('#filesend').click( function(){
        $('#filebar > .bar').replaceWith( '<div class="bar" style="width: 0%;"></div>' );
        $('#filebar').addClass( 'progress-striped' );
        $('#filebar').addClass( 'active' );
        $('#filealert').css( 'visibility', 'hidden' );
        var xhr = new XMLHttpRequest();
        if( xhr.upload ){
            xhr.upload.onprogress = function( e ){
                var done = e.position || e.loaded, total = e.totalSize || e.total;
                var perc = (Math.floor(done/total*1000)/10);
                $('#filebar > .bar').css( 'width', perc + '%' );
            };
        }
        xhr.onreadystatechange = function( e ){
            if( 4 == this.readyState ){
                $('#filebar > .bar').css( 'width', '100%' );
                $('#filebar').removeClass( 'progress-striped' );
                $('#filebar').removeClass( 'active' )
                $('#fileform').css( 'visibility', 'visible' );
                $('#filealert').css( 'visibility', 'visible' );
                refreshFileList();
            }
        };

        xhr.open( 'PUT', '/upload', true );

        var form = $('#fileform')[0];
        var fd = new FormData( form );
        xhr.send( fd );

        $('#fileform').css( 'visibility', 'hidden' );
    });

}(window.jQuery);

/* = FILE LIST ============================================================== */
!function ($) {
    "use strict"; // jshint ;_;

    refreshFileList();

}(window.jQuery);

function refreshFileList(){
    $.ajax({
        dataType: "json",
        url: '/ajax/file',
        success: function( data ) {
            var items = [];
            var files = data['files']

            $.each(files, function( key, val ) {
                items.push('<li id="' + val['id'] + '">' + val['file'] + '</li>');
            });

            var newlist = $('<ul/>', {
                'id': 'filelist',
                'class': 'unstyled',
                html: items.join('')
            });

            $('#filelist').replaceWith( newlist );
        }
    });
}
