$(document).ready(function() {

        $('[class^="percentform"]').change( function (e) { 
            var target = $(e.target);          
            var number = String(target.attr('class')).replace('percentform',''); 
            var wineClass = "winepercent" + number;
            var yearClass = "yearpercent" + number; 
            $.ajax( {
                url:'/percent/',
                timeout:5000000,
                type: 'POST',
                data: {
                    "winedjango": $('[class="' + wineClass + '"]').val(),
                    "yeardjango": $('[class="' + yearClass + '"]').val(),
                    "percentdjango": $('[class="' + target.attr('class') + '"]').val(),
                    'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(data) {
                    console.log("message");
                    console.log(data);
                    console.log(number);
                    editHTML(data,number);
                },
                error: function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                },
                traditional: true
            });
        e.preventDefault();
        });
});

function editHTML(data,number) {
  var recommendedVal = data.recommended;
  var recommendedClass = "recommended" + number;
  var marginVal = data.margin;
  var marginClass = "margin" + number;
  $('[class="' + recommendedClass + '"]').html(recommendedVal);
  $('[class="' + recommendedClass + '"]').animate({color:'#FF0000'},500);
  $('[class="' + marginClass + '"]').html(marginVal);
  $('[class="' + marginClass + '"]').animate({color:'#FF0000'},500);
}
