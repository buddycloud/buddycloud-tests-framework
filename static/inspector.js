function startInspection(){
	
	domain_url = handleDomainURL();
	$.get("/test_names", function(data){
		testsLauncher(data, domain_url);
	});
}

function testsLauncher(data, domain_url){

	handleStartTestsLauncher();
	data = JSON.parse(data);
	for ( var i=0; i<data.entries.length; i++ ){
		handleTestCreation(data.entries[i].name);
		issueTest(data.entries[i].name, domain_url);
	}
}

function issueTest(test_name, domain_url){

	$.get("/perform_test/"+test_name+"/"+domain_url, function(data){
		handleTestResponse(data);
	});
}

function handleStartTestsLauncher(){

	$("#tests_output_table").html("");
}

function handleTestCreation(test_name){

	$("#tests_output_table").append("<tr id='tr_"+test_name+"'><td>"+test_name+"</td><td id='td_"+test_name+"'></td></tr>");
}

function handleTestResponse(data){

	data = JSON.parse(data);
	$("#tr_"+data.name).attr("class", getExitStatusClass(data.exit_status));
	$("#td_"+data.name).text(data.output);
}

function handleDomainURL(){

	domain_url = $("#domain_url_box").val();
	if ( domain_url.search("://") != -1 ){
		domain_url = domain_url.substr(domain_url.search("://")+3, domain_url.length);
		$("#domain_url_box").val(domain_url);
	}
	return domain_url;
}

function getExitStatusClass(code){

	switch(code){
		case 0:
			return "success";
		case 1:
			return "error";
		default:
			return "warning";
	}
}
