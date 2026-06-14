import $ from 'jquery'
import Sigma from 'sigma'
import forceAtlas2 from 'graphology-layout-forceatlas2'
import FA2Layout from 'graphology-layout-forceatlas2/worker'
import circular from 'graphology-layout/circular'
import { sna } from './bridge.js'
import { clearDataSpace, showDataHint } from './dom.js'
import { dataVisualization } from './dataVisualization.js'
import { toGraphology } from './graphAdapter.js'

// Module singletons for the current render. drawGraph() runs on every search,
// filter and slider change, so the previous Sigma renderer + ForceAtlas2 worker
// must be torn down each time or WebGL contexts and workers leak.
let graph = null
let renderer = null
let layout = null

function destroyGraph() {
  if (layout) {
    try { layout.kill() } catch (e) { /* worker already gone */ }
    layout = null
  }
  if (renderer) {
    try { renderer.kill() } catch (e) { /* already killed */ }
    renderer = null
  }
  graph = null
}

// Equivalent of the old neovis `viz.stabilize()`: freeze the live layout so the
// nodes stop drifting (wired to the "Stop dynamic graph" button).
function stabilizeGraph() {
  if (layout) layout.stop()
}

function getNodeDimension(sn, graphType) {
  if (sn !== 'twitter') return 'nodeDegree'

  else {
    if (sn === 'twitter' && graphType === 'trafficNet')
      return sna.twNodeType
    else return 'nodeDegree'
  }
}

// Reused by both node and edge clicks. `id` is the graphology key — i.e. the
// Neo4j integer ID() as a string — handed straight back to getData.py, which
// interpolates it into "ID(n) = <id>". `kind` is 'contacts' (node) or 'links' (edge).
function handleSelect(id, kind) {
  sna.setDataViz1('selected')
  sna.setDataViz2(kind)

  let dts = JSON.parse(sna.dataToSearch)
  dts['dataViz1'] = 'selected'
  dts['dataViz2'] = kind
  sna.dataToSearch = JSON.stringify(dts)

  clearDataSpace()

  $.ajax({
    url: 'server.php',
    dataType: 'json',
    data: { dataToSearch: sna.dataToSearch, id },
    type: 'post',
    success: function (data) {
      dataVisualization(data)
    },
    error: function () {
      showDataHint(kind === 'contacts' ? 'Try to select a node' : 'Try to select a link')
    },
  })
}

function renderGraph(data, direction, dimension) {
  const container = document.getElementById('viz')
  if (!container) return

  graph = toGraphology(data, dimension, direction)

  // Sigma requires every node to have x/y. circular gives a stable, non-overlapping
  // starting ring; ForceAtlas2 then settles the real layout.
  if (graph.order > 0) circular.assign(graph)

  renderer = new Sigma(graph, container, {
    defaultEdgeType: direction ? 'arrow' : 'line',
    renderEdgeLabels: false,
    labelRenderedSizeThreshold: 1,
    // Sigma v3 disables edge events by default (perf); without this clickEdge
    // never fires and edges aren't selectable.
    enableEdgeEvents: true,
  })

  // No point running the force simulation on a single node / empty graph.
  if (graph.order > 1) {
    layout = new FA2Layout(graph, { settings: forceAtlas2.inferSettings(graph) })
    layout.start()
  }

  renderer.on('clickNode', ({ node }) => handleSelect(node, 'contacts'))
  renderer.on('clickEdge', ({ edge }) => handleSelect(edge, 'links'))
}

function drawGraph(cmd, direction, dimension) {
  destroyGraph()

  $('.content').html('<div id="viz" style="height: 100%; width: 100%"></div>')

  // The Cypher is run server-side (server.php -> runVizQuery.py) and returns
  // {nodes, rels}; the browser no longer connects to Neo4j directly.
  $.ajax({
    url: 'server.php',
    dataType: 'json',
    data: { action: 'runQuery', cmd },
    type: 'post',
    success: function (data) {
      renderGraph(data, direction, dimension)
    },
    error: function () {
      $('.content').html(
        '<div class="data-item"><span> Unable to draw the graph </span></div>'
      )
    },
  })
}

export { drawGraph, getNodeDimension, stabilizeGraph }
