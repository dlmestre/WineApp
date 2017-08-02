$(document).ready(function() {

        $("#fire_script").on('click', function (e) {
            initRotation()            
            $('#fire_script').hide();            
            $.ajax( {
                url:'/results/',
                timeout:5000000,
                type: 'POST',
                data: {
                    "django_file": $('#wineresults').val(),
                    'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(data) {
                    stopRotation();
                    console.log("message");
                    console.log(data);
                    $('#fire_script').show();               
                    htmlParserFunction(data.Result);
                    $(function(){
                        $('.table2').tablesorter();
                    });
                },
                error: function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                },
                traditional: true
            });
        e.preventDefault();
        });
});
