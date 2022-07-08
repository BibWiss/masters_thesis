//console.log(j_all.keys);

/*// texts
var texts = _.map(j_all, "text");

// create variables for all metrics
var frequencies = _.map(j_all, "frequency");
var char_lens = _.map(j_all, "char_len");
var token_counts = _.map(j_all, "token_count");
var token_lens = _.map(j_all, "token_len");
var sent_lens = _.map(j_all, "sent_len");
var pos_divs = _.map(j_all, "pos_diversity");
var sentiws = _.map(j_all, "sentiws");
var germansentiment = _.map(j_all, "germansentiment");*/

// function to show all passages texts within their own div

function getPassages() {
    var passageContainer = document.getElementById("app");
    for (var i = 0; i <= texts.length+1; i++) {
        var div = document.createElement("div");
        div.setAttribute("id", "passage_" + (i));
        div.setAttribute("class", "container");
        div.innerHTML = (`<p>${texts[i]}</p>`);
        passageContainer.appendChild(div);
    }
}

// call getPassages()
getPassages();

/*
function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
  }*/

// color definitions

var color_palette = ["#509F98", "#C16152", "#EDB85C", "#5d73b8", "#9B8945"]
var senti_colors = ["#457361", "#FFFAE8", "#96362F",]

// create charts
// https://stackoverflow.com/questions/50144861/add-border-radius-property-to-d3js-donut-chart/50145118 was very helpful here

// define Arcs, mainArc will later be layered on top of backgroundArc

var backgroundArc = d3.arc()
  .innerRadius(30)
  .outerRadius(50)
  .startAngle(0)
  .endAngle(Math.PI*2);
  
var mainArc = d3.arc()
  .innerRadius(30)
  .outerRadius(50)
  .cornerRadius(10)
  .startAngle(0)
  .endAngle(function(d) { return d/100*Math.PI* 2 });

// function addDonut() to create one donut per passage and corresponding datum using forEach
function addDonut(metrics, name, color) {
metrics.forEach((metric, index) => {
  const element_id = "#passage_"+index;
  var svg = d3.selectAll(element_id).append("svg")
    .attr("width", 100)
    .attr("height", 100);
  
  var charts = svg.selectAll("g")
    .data([metric*100])
    .enter()
    .append("g")
    .attr("class", name)
    .attr("transform","translate("+50+","+50+")");

  charts.append("path")
    .attr("d", backgroundArc)
    .attr("fill","#ccc")
    .attr("opacity",".5")

  charts.append("path")
    .attr("d", mainArc) 
    .attr("fill",color)

  charts.append("text")
    .attr('x', 1)
    .attr('y', 1)
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'central')
    .text(Math.floor(metric*100) + '%');

    svg.append("text")
      .attr('x', 0)
      .attr('y', 8)
      .attr('text-anchor', 'center')
      .attr('dominant-baseline', 'central')
      .attr("class", (name + "chart-label"))
      .attr("font-size", "12px")
      .text(name.slice(0,-2));
});
};

//define function for click on sidebar buttons

function toggleCharts(data, color, button, charts) {
var optionButton = document.getElementById(button);
optionButton.addEventListener("click", function() {if (optionButton.classList.contains("not-active")) {
  addDonut(data,charts, color); 
  optionButton.setAttribute("class", "active btn btn-secondary");
  optionButton.setAttribute("aria-pressed", "true");
} else if (optionButton.classList.contains("active")) {
  document.querySelectorAll('.' + charts).forEach(e => e.parentNode.remove(e));
  optionButton.setAttribute("class", "not-active btn btn-secondary");
  optionButton.setAttribute("aria-pressed", "false");
}
});
};

// call toggleCharts for different metrics

toggleCharts(frequencies, color_palette[0], "frequency-button", "frequency-g");
toggleCharts(char_lens, color_palette[1], "charlen-button", "charlen-g");
toggleCharts(token_lens, color_palette[2], "tokenlen-button", "tokenlen-g");
toggleCharts(sent_lens, color_palette[3], "sentlen-button", "sentlen-g");
toggleCharts(pos_divs, color_palette[4], "posdiv-button", "posdiv-g");

// same as above but for sentiment, need to consider the [-1, 1] scale

function addSentiDonut(metrics, name) {
  metrics.forEach((metric, index) => {
    const element_id = "#passage_"+index;
    var svg = d3.selectAll(element_id).append("svg")
    .attr("width", 100)
    .attr("height", 100);
    
    var charts = svg.selectAll("g")
      .data([metric*100])
      .enter()
      .append("g")
      .attr("class", name)
      .attr("transform","translate("+50+","+50+")");
  
    charts.append("path")
      .attr("d", backgroundArc)
      .attr("fill","#ccc")
      .attr("opacity",".5")
  
    charts.append("path")
      .attr("d", mainArc) 
      .attr("fill",function(){if (metric < 0) {return senti_colors[2]} else if(metric== 0){return senti_colors[1]} else if(metric > 0) {return senti_colors[0]}})
  
    charts.append("text")
      .attr('x', 1)
      .attr('y', 1)
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'central')
      .text(function(){if (metric < 0) {return "negativ"} else if(metric== 0){return "neutral"} else if(metric > 0) {return "positiv"}});

      svg.append("text")
      .attr('x', 0)
      .attr('y', 8)
      .attr('text-anchor', 'center')
      .attr('dominant-baseline', 'central')
      .attr("class", (name + "chart-label"))
      .attr("font-size", "12px")
      .text(name.slice(0,-2));
  });
  };

  function toggleSentiCharts(data, button, charts) {
    var optionButton = document.getElementById(button);
    optionButton.addEventListener("click", function() {if (optionButton.classList.contains("not-active")) {
      addSentiDonut(data, charts); 
      optionButton.setAttribute("class", "active btn btn-secondary");
      optionButton.setAttribute("aria-pressed", "true");
    } else if (optionButton.classList.contains("active")) {
      document.querySelectorAll('.' + charts).forEach(e => e.parentNode.remove(e));
      optionButton.setAttribute("class", "not-active btn btn-secondary");
      optionButton.setAttribute("aria-pressed", "false");
    }
    });
    };

toggleSentiCharts(sentiws, "sentiws-button", "sentiws-g");
toggleSentiCharts(germansentiment, "germansentiment-button", "germansentiment-g");

/*
//change bg-color function

const changeStyle = function(div, bgcolor, color) {
    div.style.backgroundColor = bgcolor;
    div.style.color = color;
}; 

// add event listeners to all passages

var ChildDivs = document.getElementById("app").getElementsByTagName('div');

for(var i=0; i< ChildDivs.length; i++ ) {
    (function () {
        var childDiv = ChildDivs[i];
        var childId = childDiv.id;
        childDiv.addEventListener("click", function() {if (document.getElementById("vis_" + childId) == null) {create_vis(childId); changeStyle(childDiv, "black", "white")} else {document.getElementById("vis_" + childId).remove(); changeStyle(childDiv, "white", "black")}}, false);
        //document.getElementById("vis_" + childId).addEventListener("click", changeStyle(childDiv, "white", "black"), false);
}());
}*/