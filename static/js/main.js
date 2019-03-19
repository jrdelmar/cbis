// ----- custom js ----- //
$(function() {
    // hide initial
    $loading = $("#loading") ;
    $error = $("#error");
    $searching = $(".searching");

    $loading.show();
    $error.hide();
    $searching.hide();

    //config - some fixed values
    const TOP_K_PREDICTIONS_SIDEBAR = 5; //top-5 results only, dont clutter my sidebar

    // check the files from the output folder
    // TODO: add a proper loading icon

    // ajax request for loading the folders in output direction
    $.ajax({
        type: "GET",
        url: "/load",
        // handle success
        success: function (result) {
            //console.log(result.results);
            var data = result.results;
            // loop through results, append to dom
            var i = 0
            for (var key in data) {
                //folder is unique so use this as the ID
                checked = ""
                if (i === 0){
                    checked = 'checked'
                }
                var content = '<tr><td><input type="checkbox" class="checkbox"  ' + checked +' /></td>';
                content = content + '<td>' + key + '</td>'; //key is the folder name
                content = content + '<td>' + data[key]["predictions"].join(",") + '</td>';
                content = content + '<td>' + data[key]["exif"].join(",") + '</td></tr>';
                $("#results").append(content);
                i++;

            }
        },
        // handle error
        error: function (error) {
            console.log(error);
            // append to dom
            $("#error").append()
        }
    });

    $loading.hide();

    //DEBUG: -----------------------------
    var search_str = "gun,church, scuba diver, water";
    var parse_me = {
        'WEAPON-DB9_20190226_180745': {
            'predictions': ["predictions_20190223_234941.csv"],
            'exif': ["exif_20190223_234941.csv"]
        }
    }
    var data = JSON.stringify({files: parse_me, search_list: search_str})
    //search(data);

    //dynamic links
    //$(".item").live("click", function(e) {
    $(".show_info").live("click", function(e) {
        // do something
        e.preventDefault();

        //filename
        //var title = $(this).text().split(" ")[0]
        var title = $(this).find('img').attr("title").split(" ")[1]
        $("#file-info-label").html(title); //fname title

        //get the img url
        var img_src = decodeURIComponent ($(this).find('img').attr("src"));
        var pred_file = $(this).find('img').attr("data-file-pred");
        var exif_file = $(this).find('img').attr("data-file-exif");

        //remove other active classes
        $("#thumbs").find('img').removeClass('img-active');
        //add active class on this item that I just clicked
        $(this).find('img').addClass('img-active');

        var parameters = { img : img_src , pred_file: pred_file, exif_file: exif_file }

        //search for exif information etc for this item
        $.ajax({
            type: "POST",
            url: "/display",
            data : parameters,
            // handle success
            success: function (result) {
                //console.log('result.results=',result.results);
                var predictions = result.predictions;
                var exif_info = result.exif_info; //[col,values]
                var map_path = result.map_path; //[col,values]
                var gps_coordinates = result.gps_coordinates; //lat, lon

                //console.log("result_list=>", result.predictions)
                load_prediction_table(predictions, TOP_K_PREDICTIONS_SIDEBAR);

                $("#exif-placeholder").fadeOut(); //always available so delete the placeholder
                load_exif_table(exif_info);

                //clear map content first
                $("#map-info").html("");
                if(map_path !== "" && gps_coordinates[0] !== 0 && gps_coordinates[1] !== 0 ){
                    load_gps_map(map_path, gps_coordinates);
                    $("#map-placeholder").fadeOut();
                } else {
                    $("#map-placeholder").show();
                }
            },
            // handle error
            error: function (error) {
                console.log(error);
                // append to dom
                $("#error").append()
            }
        });

    });

    //TODO: disable/enable the button if at least one checkbox is checked
    $("#search-submit").click(function () {
        var parse_me = {}
        $('#results tr').filter(':has(:checkbox:checked)').each(function () {
            var f = $(this).find("td").eq(1).html(); //folder
            var p = $(this).find("td").eq(2).html();  //predictions
            var e = $(this).find("td").eq(3).html(); //exif
            /* files = {'foldername':{'predictions' = [],'exif'=[]}}
             */
            //console.log(f)
            parse_me[f] = {'predictions': p.split(","), 'exif': e.split(",")}
        });

        if (isEmpty(parse_me)) {
            //alert("TODO: Error-handling!")
            $("#parse-error").html("Nothing to parse. Tick at least one of the checkboxes above.");
        } else {
            $("#parse-error").html("");
            //delete previous results
            $('.item-thumbs').remove(); //joanna

            //TODO: make sure this is not empty
            var search_str = $("#search-list").val();
            if(isEmpty(search_str)){
                //alert("TODO: Error-handling!")
                $("#search-error").html("You get what you give. There is nothing to parse, so returning nothing.");
            } else {
                $loading.show();
                var data = JSON.stringify({files: parse_me, search_list: search_str});
                //clear the content
                search(data); //start search data using ajax
            }
        }
    });

    //change the width of the image
    $('.size-change').click(function (e)  {
        $('#content img').css({'max-width': $(this).attr("data-id")})
    });


});//on-load event

//how to reload css

function load_prediction_table(data, top_k ){

    //$("#empty-row-placeholder").remove();
    //remove all rows
    $("#file-info-table > tbody").empty();

    //var data = [['church','house'],[0.9967,0.8909]];
    var labels = data[0];
    var probs = data[1];
    var row = "";

    //append to the table
    for (i = 0; i < labels.length; i++) {
        row = "<tr><td>" + (i+1) + "</td><td>" + labels[i] + "</td><td>" + probs[i] + "</td></tr>"
        $("#file-info-body").append(row)
        if (i == (top_k - 1)){
            break
        }
    }
}

function load_exif_table(data){
    //from the app: [col,values]
    // convert to this format:
    // var data = [
    //     [
    //         "Tiger Nixon",
    //         "System Architect"
    //     ],
    //     [
    //         "Garrett Winters",
    //         "Director"
    //     ]
    // ]
    col = data[0];
    val = data[1];
    exif_row = [];
    for (i = 0; i < col.length; i++){
        _col = col[i]
        _val = val[i]
        exif_row.push ([_col, _val])
        //console.log("col=", col[i], " val=", val[i])
    }
    //destroy when it's already created
    var $exifInfo = $('#exif-info');
    if($.fn.DataTable.isDataTable("#exif-info")){
        $exifInfo.DataTable().clear().destroy();
    }
    $exifInfo.DataTable( {
            iDisplayLength: 20,
            data: exif_row,
            columns: [
                { title: "Exif Information" },
                { title: "Value" }
            ],
            dom: 'Bfrtip',
            buttons: [
                'print'
            ]
    } );
}

function load_gps_map(map_path, [lat, lon]){
    content = '<span class="align-left"><a href="' + map_path + '">' +
'                <i class="icon-cloud-download icon-circled icon-bglight icon"></i></a></span>' +
'            <span>' +
'              Latitude: ' + lat.toString() +
'              Longitude: ' + lon.toString() +
'              <img src="' + map_path + '" alt="" />' +
'            </span>';

    $("#map-info").html(content);

}

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

function find_info_file(filename, data){
    var p_file = "";
    var e_file = "";
    /* expected data:
    {exif: [0: {exif_file: [image_list] } ],
    predictions:
        [0: {pred_file: [image_list] } ,
         1: {pred_file1: [image_list] }]}
     */
    for (var k in data) {
       for (var i in data[k]) {
           for (var j in data[k][i]) {
               var is_found = jQuery.inArray(filename, data[k][i][j]);
               if (is_found >= 0) {
                   if (k === "predictions") {
                       p_file = j;
                       break;
                   } else {
                       e_file = j;
                       break;
                   }
               }
           }
       }
    }
    return [p_file, e_file]
}

/**
 * search the prediction files and return the image list
 * @param data
 */
function search(data){
    var dataset_search = []; //for dataset visualisation
    var $dataset_search
    $.ajax({
        type: "POST",
        url: "/search",
        contentType: 'application/json',
        data: data,
        // handle success
        success: function (result) {
            //console.log('result.results=',result.results);
            var data = result.results;

            //console.log('data=',data)
            if (0 === data.length) {
                //TODO: Error handling
                alert("No results found");
            }

            var result_list = result.result_list;
            generate_filter_list(data);
            /**
             * <li class="all active"><a href="#">All (40)</a></li>
             <li class="gun"><a href="#" title="">Guns (21)</a></li>
             <li class="church"><a href="#" title="">Church (19)</a></li>
             */

            console.log("Total images found:", data.length);
            //------ for visualisation ------
            var dataset_label = []; //for dataset visualisation
            //var dataset_search = []; //for dataset visualisation
            var arr_label = []; //container for labels added
            var arr_search = []; //container for labels added
            var imagenet_guns = ["revolver","assault_rifle","rifle","muzzle"];
            //------ end of visualisation ------

            for (i = 0; i < data.length; i++) {
                // console.log('fname=',data[i][0]);
                // console.log('label=',data[i][1]);
                // console.log('prediction=',data[i][2]);

                var file = data[i][0];
                var label = data[i][1];
                var probability = data[i][2];
                var search_label = data[i][3];
                var icon_size = data[i][4];

                var data_id = "id-" + i;
                var caption = "Display Information";//"Label: " + label + "(" + (probability) + ")";

                var filename = file.split('/').pop().split('\\').pop();
                //console.log("file:", file, "filename:", filename, " search_label=",search_label)

                //prediction file to be used later
                var files  = find_info_file(file, result_list)
                var pred_file = files[0];
                var exif_file = files[1];

                var prob = (probability* 100 ).toPrecision(4);
                var item_label = "";//"<p><strong>" + filename + "</strong> " + label + " (" + prob + "%)</p>"
                var item_label_title = "File: "+ filename + " Label: "+label + " (" + prob + "%)";
                //append results
                //console.log(file, filename, file.replace(filename, encodeURI(filename)))
                var encodedFile = file.replace(filename, encodeURI(filename))

                var icons = '<div class="text-left clear-marginbot marginbot10"><span class="file-info show_info">' +
                    '<a href="#" title="' + caption + '"><i class="icon-file icon-circled icon-bglight icon"></i></a></span> '
                    + '<span><a class="download" href="' + encodedFile + '" title="Download '+ filename + '"><i class="icon-cloud-download icon-circled icon-bglight icon"></i></a></span></div>'
                var content = '<li class="item-thumbs span2 design" data-id="' + data_id + '" data-type="'+ search_label +'">'
                            +'<div class="item" id="img-label-' + data_id + '">' + item_label + icons
                            +'<div class="show_info"><img title="'+item_label_title+'" src="' + encodedFile + '" alt="" data-file-pred="' + pred_file
                            +'" data-file-exif="' + exif_file + '" /></div></div></li>';

                $('#thumbs').append(content);

                //------ for visualisation ------
                var idx_search = $.inArray(search_label, arr_search);
                var idx_category = $.inArray(label, imagenet_guns);

                if(idx_search > -1){ //found it, then just add
                    dataset_search[idx_search]["value"] = (dataset_search[idx_search]["value"])  + 1
                } else {
                    arr_search.push(search_label)  //ensures same index
                    var category = "not_gun";
                    if(idx_category >-1){ category = "gun" }
                    dataset_search.push({"label": search_label,"value": 1, "category":category})
                }
                //------ end of visualisation ------
            }
            $dataset_search = dataset_search
            //call the animation function again here
            call_thumbs_animation();
            //visualise only after its done, move to complete function
            //visualize_results(dataset_search);
            scrollToDiv($("#search-results-title"));
        },
        // handle error
        error: function (error) {
            console.log(error);
            // append to dom
            $("#error").append()
        },
        //oncomplete
        complete: function (){
            $loading.hide();
            visualize_results($dataset_search);
        }
    });

}


function generate_filter_list(data){
    // var file = data[i][0];
    // var label = data[i][1];
    // var probability = data[i][2];
    // var search_label = data[i][3];
    var search_label = {all:0,gun:0 }; //default all and gun are included even if there is no gun search

    $.each(data, function(i, item) {
        var label = item[3];
        if (label in search_label) {
            search_label[label] = search_label[label] + 1
        } else {
            //add a new label then add
            search_label[label] = 1
        }

        //always add to all
        search_label['all'] = search_label['all'] + 1

    });

    console.log(search_label)
    /**
     * <li class="all active"><a href="#">All (40)</a></li>
     <li class="gun"><a href="#" title="">Guns (21)</a></li>
     <li class="church"><a href="#" title="">Church (19)</a></li>
     */
    $("#thumbs-categ-filter").html("") //clear this first
    $.each(search_label, function(i, val) {
        var active = (i.toString() === "all") ? 'active' : '';
        var content = '<li class="' + i + ' '+active+'"><a href="#">'+i+' (' + val + ')</a></li>'

        $("#thumbs-categ-filter").append(content)
    });
}


//Call the function again because the elements were dynamically loaded
function call_thumbs_animation(){
    if (jQuery().quicksand) {
        // Clone applications to get a second collection
        var $data = $(".portfolio").clone();
        //NOTE: Only filter on the main portfolio page, not on the subcategory pages
        $('.filter li').click(function(e) {
            $(".filter li").removeClass("active");
            // Use the last category class as the category to filter by. This means that multiple categories are not supported (yet)
            var filterClass=$(this).attr('class').split(' ').slice(-1)[0];

            if (filterClass == 'all') {
                var $filteredData = $data.find('.item-thumbs');
            } else {
                var $filteredData = $data.find('.item-thumbs[data-type=' + filterClass + ']');
            }
            //BUG-FIX:  manually filter by checking duplicate ids because of dynamic content
            var arr = [];
            var deleteArr = [];
            $.each($filteredData, function(i, item){
                if($.inArray(item.dataset.id, arr) > -1){
                    //store the elements to be deleted, do not delete here because it messes up the indexes
                    deleteArr.push(i)
                } else {
                    arr.push(item.dataset.id)
                }
            });

            deleteArr = deleteArr.sort(function(a, b){return b-a}) //descending order
            $.each(deleteArr, function(i, item){
                $filteredData.splice(item,1)
            });
            //BUG-FIX -- end --

            $(".portfolio").quicksand($filteredData, {
                duration: 600,
                adjustHeight: 'auto'
            }, function () {

                //$("a[data-pretty^='prettyPhoto']").prettyPhoto();

            });

            $(this).addClass("active");
            return false;
        });

    }//if quicksand
}

function visualize_results(dataset){
    if (dataset != null){
        if (dataset.length > 0){
            $("#section-chart-search").show();
            $("#chart-search").html(""); //clear content first
            //refresh links
            createBubbleChartFromData({'children': dataset},'#chart-search' )
        }else {
            $("#section-chart-search").hide();
        }
    }

}

