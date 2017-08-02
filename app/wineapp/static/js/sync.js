$(document).ready(function() {
    console.log("sync");
        $("#syncdb").on('click', function (e) {
            console.log("it works!");            
            initRotation();
            $('#syncdb').hide();            
            $.ajax( {
                url:'/syncoutput/',
                timeout:5000000,
                success: function(data) {
                    stopRotation();
                    console.log("message");
                    console.log(data);
                    $('#syncdb').show();               
                    console.log(data.Records);
                    console.log(data.Time);
                    getData(data.Records,data.Time);                    
                },
                error: function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                },
                traditional: true
            });
        e.preventDefault();
        });
});
