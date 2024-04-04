const { ipcRenderer } = require("electron");

const fileButton = document.getElementById("choose-file");
const demoButton = document.getElementById("demo");
const runButton = document.getElementById("run");
const backButton = document.getElementById("back-intro");
const introDiv = document.getElementById("intro-box");
const controlDiv = document.getElementById("graph-control");
const bpmTolerance = document.getElementById("bpm-tolerance");
const keyTolerance = document.getElementById("key-tolerance");

fileButton.onclick = () => {
  ipcRenderer.send("open-file-dialog");
};

demoButton.onclick = () => {
  ipcRenderer.send("run-demo");
};

runButton.onclick = () => {
  ipcRenderer.send("run");
};

backButton.onclick = () => {
  d3.select("svg").remove();
  introDiv.style.visibility = "visible";
  introDiv.style.display = "block";
  controlDiv.style.visibility = "hidden";
};

bpmTolerance.addEventListener("change", (event) => {
  ipcRenderer.send("bpm-change", event.target.value);
});

keyTolerance.addEventListener("change", (event) => {
  ipcRenderer.send("key-change", event.target.value);
});

ipcRenderer.on("file-selected", (event, filePath) => {
  const filePathElement = document.getElementById("file-path");
  filePathElement.textContent = filePath;
  runButton.disabled = false;
});

ipcRenderer.on("graph-received", (event, data) => {
  visualise(data);
});

function visualise(data) {
  introDiv.style.visibility = "hidden";
  introDiv.style.display = "none";
  controlDiv.style.visibility = "visible";
  d3.select("svg").remove();

  const width = window.innerWidth;
  const height = window.innerHeight;

  const simulation = d3
    .forceSimulation()
    .nodes(data.nodes)
    .force("link", d3.forceLink(data.links).id((d) => d.id))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));

  const svg = d3
    .select("body")
    .append("svg")
    .attr("id", "graph-svg")
    .attr("width", width)
    .attr("height", height)
    .call(d3.zoom().on("zoom", (event) => svg.attr("transform", event.transform)));

  const link = svg
    .append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(data.links)
    .join("line")
    .attr("stroke-width", 1);

  const node = svg
    .append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(data.nodes)
    .join("circle")
    .attr("r", 5)
    .attr("fill", "steelblue")
    .call(drag(simulation));

  simulation.on("tick", () => {
    link
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
  });

  function drag(simulation) {
    function dragStarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event) {
      const scale = d3.zoomTransform(svg.node()).k;
      event.subject.fx = event.x / scale;
      event.subject.fy = event.y / scale;
    }

    function dragEnded(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    return d3
      .drag()
      .on("start", dragStarted)
      .on("drag", dragged)
      .on("end", dragEnded);
  }

  const centreButton = document.getElementById("centre");
  centreButton.addEventListener("click", () => {
    d3.select("svg").remove();
    visualise(data);
  });
}