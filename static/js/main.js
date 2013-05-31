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

        xhr.open( 'PUT', '/ajax/file', true );

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
            var items1 = [];
            var items2 = [];
            var files = data['files']

            $.each(files, function( key, val ) {
                items1.push('<li>' + val['file'] + '</li>');
                items2.push('<option value="' + val['id'] + '">' + val['file'] + '</option>');
            });

            var newlist = $('<ul/>', {
                'id': 'filelist',
                'class': 'unstyled',
                html: items1.join('')
            });

            $('#filelist').replaceWith( newlist );

            var newformlist = $('<select/>', {
                'id': 'jobfile',
                'name': 'file',
                html: items2.join('')
            });

            $('#jobfile').replaceWith( newformlist );
        }
    });
}

/* = JOB STUFF ============================================================== */
!function ($) {
    "use strict"; // jshint ;_;

    $('#jobstart').click( function(){
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function( e ){
            if( 4 == this.readyState ){
                alert( "job sended" );
                refreshJobList();
            }
        };

        xhr.open( 'POST', '/ajax/job', true );

        var form = $('#jobform')[0];
        var fd = new FormData( form );
        xhr.send( fd );
    });

    refreshJobList();

}(window.jQuery);

function refreshJobList(){
    $.ajax({
        dataType: "json",
        url: '/ajax/job',
        success: function( data ) {
            var items = [];
            var jobs = data['jobs']

            $.each( jobs, function( key, val ) {
                items.push('<li>' + val['id'] + '</li>');
            });

            var newlist = $('<ul/>', {
                'id': 'joblist',
                'class': 'unstyled',
                html: items.join('')
            });

            $('#joblist').replaceWith( newlist );
        }
    });
}

/*=========================================================================== */
