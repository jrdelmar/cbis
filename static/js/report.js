// ----- report js ----- //
$(function() {
    //on-load do not display
    $("#section-chart-vis").hide();
    $("#section-chart-search").hide();
    $("#section-chart-heatmap").hide();


    $('#graph-submit').click(function() {

        var prediction_files = {}
        //find the checked prediction files
        var pfiles = []
        var folders = []
        $('#results tr').filter(':has(:checkbox:checked)').each(function () {
            var f = $(this).find("td").eq(1).html(); //folder
            var p = $(this).find("td").eq(2).html();  //predictions
            //var e = $(this).find("td").eq(3).html(); //exif
            prediction_files[f] = {'predictions': p.split(",")}
            pfiles.push(p);
            folders.push(f);
        });

        //check that there is a checkbox
        if (isEmpty(prediction_files)) {
            $("#parse-error").html("Nothing to parse. Tick at least one of the checkboxes above.");
        } else {
            $("#parse-error").html("");
            $loading.show();
            /*
             * {
             * WEAPON-DB9_20190226_180745: {predictions: ["predictions_20190223_234941.csv"]},
             * WEAPON-DB3_20190226_180745: {predictions: ["predictions_20190225_013906.csv"]}
             * }
             */
            const params = jQuery.param({
                folders: folders.join(","),
                pfiles: pfiles.join(","),
                k: "20"
            });

            scrollToDiv($("#vis-title"));
            $("#vis").html(""); //clear content first
            $("#heatmap").html(""); //clear content first

            createBubbleChartFromUrl(params, '#vis');


            $("#section-chart-vis").show();
            $("#section-chart-heatmap").show();


        }
    });

}); //--end of function


function scrollToDiv(target){
    if (target != undefined){
        $('html,body').animate({
            scrollTop: target.offset().top
        }, 1000)
    }
}

//used in report screen
function createBubbleChartFromUrl(params,selector){

    var myBubbleChart = bubbleChart();
    function display(error, data) {
        if (error) {
            console.log(error);
        }
        myBubbleChart(selector, data.children);
        $loading.hide();

        $('.item-thumbs').remove(); //remove old images

        //display after render
        createHeatMap();

        //display after finishing
        display_random_images(data.random_images);



    }
    //var params="folders=WEAPON-DB9_20190226_180745&pfiles=predictions_20190223_234941.csv&k=20"
    d3.json("/visualise?" + params, display);
    // setup the buttons.
    setupButtons(myBubbleChart);
}

function createBubbleChartFromData(data,selector){
    var myBubbleChart = bubbleChart();
    myBubbleChart(selector, data.children);
    // setup the category buttons.
    setupButtons(myBubbleChart);
}

function createHeatMap(){

    d3.json("/heatmap", function(data) {
        //console.log(data.children.length)
        v3heatmap(  data.children, '#heatmap');

    });
}



/*
 * Sets up the layout buttons to allow for toggling between view modes.
 */
function setupButtons(myBubbleChart) {

    //refresh the buttons
    $("#toolbar li").removeClass("active");
    $("#toolbar #all").addClass("active");

    d3.select('#toolbar')
        .selectAll('.chart-links')
        .on('click', function () {
            // Remove active class from all buttons
            d3.selectAll('.chart-links').classed('active', false);
            // Find the button just clicked
            var button = d3.select(this);
            // Set it as the active button
            button.classed('active', true);
            // Get the id of the button
            var buttonId = button.attr('id');

            // Toggle the bubble chart based on
            // the currently clicked button.
            myBubbleChart.toggleDisplay(buttonId);
        });
}

function display_random_images(image_list){
    for (var k in image_list) {
        var file = image_list[k]
        var filename = file.split('/').pop().split('\\').pop();
        var encodedFile = file.replace(filename, encodeURI(filename))
        var content = '<li class="item-thumbs span1 design">'
                    +'<div class="item">'
                    +'<img title="' + filename +'" src="' + encodedFile + '" alt="" /></div></li>';

        $('#thumbs-sample').append(content);

    }




}

