var width = "100%", height = 150;

var svg = d3.select("#test_launcher_status").append("svg")
	.attr("width", width)
	.attr("height", height)
	.append("g")
	.attr("transform", "translate(10, " + (height / 2) + ")");

function updateDisplay(new_data, status) {

	if ( status != "intro" ){

		var old_data = svg.selectAll("text").data();

		var common = _.union(new_data, old_data);

		var text = svg.selectAll("text")
			.data(common, function(d){ return d; });

		transitions(text, 400, status);

		window.setTimeout(function(){
			var text = svg.selectAll("text")
				.data(new_data, function(d){ return d; });
			transitions(text, 750, status);
		}, 400);

	}
	else{
		
		var text = svg.selectAll("text")
			.data(new_data, function(d){ return d; });
		transitions(text, 1200, status);
	}
}

function transitions(text, dur, status){

	text.attr("class", "update")
		.transition()
			.duration(dur)
			.attr("x", function(d, i) { return i * ((status == "intro")? 32 : 16); })
			.attr("class", ((status == "info")?
						"enter"   :
						((status == "intro")?
						 	"intro"      :
							"exit"
						)
					))

	text.enter().append("text")
			.attr("class", ((status == "info")?
						"enter"   :
						((status == "intro")?
						 	"intro"      :
							"exit"
						)
					))
		.attr("dy", ".35em")
		.attr("y", -60)
		.attr("x", function(d, i) { return i * ((status == "intro")? 32 : 16); })
		.style("fill-opacity", 1e-6)
		.text(function(d) { return d; })
		.transition()
			.duration(dur)
			.attr("y", 0)
			.style("fill-opacity", 1)

	text.exit()
		.attr("class", "exit")
		.transition()
			.duration(dur)
			.attr("y", 60)
			.style("fill-opacity", 1e-6)
			.remove();

}
