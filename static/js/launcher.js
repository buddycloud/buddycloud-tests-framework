var lastResults = null;

function getUpdatedResults(cancelling){

    if ( !RUN_ID ){
        return;
    }

    $.ajax({
        url: "/get_results/" + RUN_ID,
        type: "get",
        dataType: "json",
        success: function(data){
            lastResults = data;
            handleResults(data, cancelling);
        },
        error: function(jqXHR){
            if (lastResults != null){
                handleResults(lastResults, true);
            }
            if (updaterId != null){
                clearInterval(updaterId);
            }
            finishLauncher();
        }
    });

}

var updaterId = null;

// Get tests from server and starts tests launcher
function startInspection(){

    domain_url = handleDomainURL();
    if ( domain_url == null ){
        return;
    }
    $("#inspect_button").addClass("active");
    $("#inspect_button").removeClass("disabled");
    $("#inspect_button").text("Stop");
    $("#inspect_button").attr("onclick", "");
    $("#domain_url_box").prop('disabled', true);
    $.ajax({
        url: "/launch/" + domain_url,
        type: "POST",
        dataType: "json",
        success: function(data){
            RUN_ID = data.run_id;
            getUpdatedResults(false);
            updaterId = window.setInterval(function(){
                getUpdatedResults(false);
            }, 5000);
        },
        error: function(jqXHR){
            if (updaterId != null){
                clearInterval(updaterId);
            }
            if ( jqXHR.status == 503 ){
                window.setTimeout(function(){
                    startInspection();
                }, 5000);
            }
            else {
                $("#inspect_button").attr("onclick", "startInspection();");
                $("#inspect_button").removeClass("active");
                $("#inspect_button").text("Check");
                $("#domain_url_box").prop('disabled', false);
            }
        }
    });
}

function stopInspection(){

    getUpdatedResults(true);
    $.ajax({
        url: "/stop_launcher/" + RUN_ID,
        type: "POST",
        success: function(data){
            if (updaterId != null){
                clearInterval(updaterId);
            }
            finishLauncher();
        },
        error: function(jqXHR){
            if ( jqXHR.status == 503 ){
                window.setTimeout(function(){
                    stopInspection();
                }, 5000);
            }
        }
    });
}
