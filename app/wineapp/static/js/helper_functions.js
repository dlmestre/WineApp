var phrases = new Array("retrieving results", "parsing information", "formatting table");
var index = 0;
var interval = null;

function initRotation() {
    $("#output").html("<h3><code>loading</code></hÂ3>");
    interval = setInterval(rotate,2000);
}

function stopRotation() {
    clearInterval(interval);
    $('#output').html("");
}

function rotate() {
    var phrase = phrases[(index++)%(phrases.length)];
    $('#output').html("<h3><code>"+phrase+"</code></h3>");
}

function getData(records,time) {
    var link = '<a href="http://54.199.166.85/gettable/">Table Page<a>';
    var phrase = "<p>Django took "+time+" seconds to extract "+records+" records.</p><p> You can find the results here: </p> " + link;
    $('#output').html("<code"+phrase+"</code>");
}

function htmlParserFunction(data) {
    var part1 = '<table class="table2 table table-striped"><thead><tr><th>Wine</th><th>Region</th><th>Vintage</th>';
    var part2 = '<th>Format</th><th>Cost</th><th>Lowest WS Price</th><th>Recommended Selling Price</th>';
    var part3 = '<th>Markup (%)</th><th>Markup Price</th><th>Margin HKD</th><th>Sell</th><th>WS Merchants</th>';
    var part4 = '<th>Quantity</th><th>Type</th><th>Vendor</th></thead><tbody>';

    var trHTML = part1 + part2 + part3 + part4;

    $.each(data, function (i, item) {
        var Merchs = [];
        wineHTML = '<tr><td>'+item.Wines+'</td>';
        regionHTML = '<td>'+item.Regions+'</td>';
        vintageHTML = '<td>'+item.Years+'</td>';
        formatHTML = '<td>'+item.Formats+'</td>';
        costHTML = '<td>'+item.Prices+'</td>';
        lowestWSpriceHTML = '<td>'+item.PricesMin[0]+'</td>';
        recommendedPriceHTML = '<td>'+item.Recommended+'</td>';
        markupPercentilesHTML = '<td>'+item.Percentiles+'</td>';
        markupsPricesHTML = '<td>'+item.Markups+'</td>';
        marginHKDHTML = '<td>'+item.Margin+'</td>';
        sellHTML = '<td>'+item.Sell+'</td>';
        for (var i = 0; i < item.Merchants.length; i++) {
            if (item.Links[i] == "N/A") {
                string = '<a style="target-new: tab;">N/A</a>';
            } else {
                string = '<a href="'+item.Links[i]+'" target="_blank" style="target-new: tab;">'+item.Merchants[i]+'</a>';
            }
            Merchs.push(string);
        }
        merchantsHTML = '<td>'+Merchs.join(" - ")+'</td>';
        quantityHTML = '<td>'+item.Quantity+'</td>';
        typeHTML = '<td>'+item.Type+'</td>';
        vendorHTML = '<td>'+item.Vendor+'</td>';

        var partHTML1 = wineHTML + regionHTML + vintageHTML + formatHTML + costHTML + lowestWSpriceHTML;
        var partHTML2 = recommendedPriceHTML + markupPercentilesHTML + markupsPricesHTML + marginHKDHTML;
        var partHTML3 = sellHTML + merchantsHTML + quantityHTML + typeHTML + vendorHTML;
        trHTML += partHTML1 + partHTML2 + partHTML3 +'</tr>';
    });

    trHTML = trHTML+'</tbody></table>';
    $('.selectorAjax').append(trHTML);
    $('#downloadtable').append('<div class="downloadbutton"><a href="/download2">Download</a></div>');
}

/*
downloadtable
FinalDictionary["Raw"] = results
        FinalDictionary["Wines"] = wines
        FinalDictionary["Prices"] = prices
        FinalDictionary["Years"] = years
        FinalDictionary["Merchants"] = merchants
        FinalDictionary["PricesMin"] = prices_lower
        FinalDictionary["Bottles"] = bottles
        FinalDictionary["Links"] = links
        FinalDictionary["Dictionary"] = dictionary_wines
*/
