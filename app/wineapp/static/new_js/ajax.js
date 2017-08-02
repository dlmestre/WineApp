$(document).ready(function() {
    $("#fire_script").on('click', function (e) {
        var msg = $('.progressmsg');           
        console.log("script fired!");
        console.log('{{ csrf_token }}');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        console.log(token);

        var formData = new FormData($("#formdata")[0]);
        formData.append('csrfmiddlewaretoken',token);
        console.log(formData);
        msg.html("<p style='color:red;'>Uploading File</p>");
        $.ajax( {
            url:'/uploadfile/',
            timeout:5000000,
            mimeType: "multipart/form-data",
            contentType: false,
            cache: false,
            processData: false,
            type: 'POST',
            data: formData,
            xhr: function() {
                var myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload){
                    myXhr.upload.addEventListener('progress',progress, false);
                }
                return myXhr;
            },
            success: function(json) {
                console.log("content:");
                console.log(json);
                secondajax(json);
                console.log("success");
            },
            error: function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            },
            traditional: true
        });
    e.preventDefault();
    });
});

function secondajax(json) {
    var msg = $('.progressmsg');
    var percent = $('#percent');
    json = JSON.parse(json);
    console.log(json);
    console.log(json.keywords);
    console.log(json["keywords"]);
    console.log("Second part!");
    var token = $("input[name=csrfmiddlewaretoken]").val();
    console.log(token);
    var formData2 = new FormData($("#formdata")[0]);
    formData2.append('csrfmiddlewaretoken',token);
    formData2.append('keywords',json.keywords);
    formData2.append('time',json.size*0.0025)    
    console.log(formData2);
    console.log("accessing second form");
    $.ajax( {
        url:'/uploadkeywords/',
        timeout:5000000,
        type: 'POST',
        mimeType: "multipart/form-data",
        contentType: false,
        cache: false,
        processData: false,
        data: formData2,
        xhr: function() {
            var myXhr = $.ajaxSettings.xhr();
            if(myXhr.upload){
                myXhr.upload.addEventListener('progress',progress, false);
            }
            return myXhr;
        },
        success: function(json2) {
            percent.attr('aria-valuenow', 0);
            percent.html("");
            percent.width("0%");
            msg.html("<p style='color:red;'>The keywords were inserted into DB</p>");
            console.log("message");
            console.log(json2);
        },
        error: function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        },
        traditional: true
    });
}

function progress(e){
    var percent = $('#percent');
    var msg = $('.progressmsg');
    if(e.lengthComputable){
        var max = e.total;
        var current = e.loaded;

        var Percentage = (current * 100)/max;

        var RoundedPercentage = Math.round(Percentage) + '%';
        console.log(Percentage);

        console.log("Upload Progress");
        percent.width(RoundedPercentage);
        percent.html(RoundedPercentage);
        percent.attr('aria-valuenow', Percentage);
        if(Percentage >= 100)
        {
           msg.html("<p style='color:red;'>File Uploaded, starting sending keywords to DB</p>");  
        }
    }  
 }
