// Converts the {nodes, rels} JSON returned by server/dataSearcher/runVizQuery.py
// into a graphology graph that Sigma.js renders. This is the port of the old
// neovis.js `labels`/`relationships` config: it encodes which property drives a
// node's caption and size, and which property drives an edge's thickness.
//
// CRITICAL: a node's graphology key is its Neo4j integer ID() (as a string).
// Sigma's clickNode/clickEdge events hand that key straight back, and
// getData.py interpolates it into "ID(n) = <id>" — so the key MUST stay the
// integer ID() or node selection (the side .data panel) breaks silently.

import { MultiGraph, MultiDirectedGraph } from 'graphology'

// Node label -> property used as the visible caption (from the neovis `labels` config).
export const NODE_CAPTION_BY_LABEL = {
  // facebook
  Friend: 'name', RemovedFriend: 'name', Post: 'timestamp', FriendPost: 'timestamp',
  Comment: 'timestamp', Direct_Message: 'timestamp', fbUser: 'name',
  // twitter
  twUser: 'username', Liked_Tweet: 'tweet', Tweet: 'created_at', Retweet: 'created_at',
  BothFollowType: 'screen_name', Follower: 'screen_name', Following: 'screen_name',
  // mbox
  Undirected_Node: 'label', Directed_Node: 'label',
}

// Labels whose node size scaled with the `dimension` property in the old config
// (nodeDegree / retweet_count). Labels not listed here had a fixed size (fbUser,
// twUser, Liked_Tweet — the hub/leaf nodes).
export const NODE_SIZEABLE = new Set([
  'Friend', 'RemovedFriend', 'Post', 'FriendPost', 'Comment', 'Direct_Message',
  'Tweet', 'Retweet', 'BothFollowType', 'Follower', 'Following',
  'Undirected_Node', 'Directed_Node',
])

// Relationship type -> property used as the edge thickness (from the neovis
// `relationships` config). All edges had caption:false (no edge labels).
export const REL_THICKNESS_BY_TYPE = {
  PUBLISHED: 'count', TAGGED_IN: 'count', FRIEND: 'count',
  TAG: 'tagged_together', TAGGED_TOGETHER: 'tagged_together', FBUSERFRIEND: 'tagged_together',
  LIKED_TWEET: 'count', TWEETED: 'count', QUOTED: 'count', FOLLOW_FOR_ALL_USERS: 'count',
  FOLLOW: 'count', FOLLOWING: 'count', SAME_ACCOUNT: 'count',
  UNDIRECTED_EDGE: 'edge_weight', DIRECTED_EDGE: 'edge_weight',
}

// A distinct color per label so node types stay separable (neovis colored by
// vis group). Unmapped labels fall back to grey.
const COLOR_BY_LABEL = {
  fbUser: '#1877f2', Friend: '#42b72a', RemovedFriend: '#e4506f', Post: '#f5a623',
  FriendPost: '#f7b955', Comment: '#9b59b6', Direct_Message: '#e67e22',
  twUser: '#1da1f2', Tweet: '#17bf63', Retweet: '#794bc4', Liked_Tweet: '#e0245e',
  Follower: '#657786', Following: '#8899a6', BothFollowType: '#ffad1f',
  Undirected_Node: '#2c82c9', Directed_Node: '#16a085',
}
const DEFAULT_COLOR = '#9aa0a6'
const EDGE_COLOR = '#c4c4cc'

const NODE_SIZE_RANGE = [4, 22]
const NODE_DEFAULT_SIZE = 12
const EDGE_SIZE_RANGE = [2, 7]
const EDGE_DEFAULT_SIZE = 2

function num(v) {
  const n = parseFloat(v)
  return isNaN(n) ? null : n
}

function minMax(values) {
  let min = Infinity
  let max = -Infinity
  for (const v of values) {
    if (v < min) min = v
    if (v > max) max = v
  }
  return [min, max]
}

function linearScale(v, inMin, inMax, outMin, outMax) {
  if (inMax <= inMin) return (outMin + outMax) / 2
  const t = (v - inMin) / (inMax - inMin)
  return outMin + t * (outMax - outMin)
}

function captionFor(node) {
  for (const label of node.labels) {
    const prop = NODE_CAPTION_BY_LABEL[label]
    if (prop && node.properties[prop] != null) return String(node.properties[prop])
  }
  return node.labels[0] || node.id
}

function colorFor(node) {
  for (const label of node.labels) {
    if (COLOR_BY_LABEL[label]) return COLOR_BY_LABEL[label]
  }
  return DEFAULT_COLOR
}

// Returns the raw numeric size property for a node if any of its labels scales,
// else null (fixed-size node).
function sizeablePropValue(node, dimension) {
  for (const label of node.labels) {
    if (NODE_SIZEABLE.has(label)) return num(node.properties[dimension])
  }
  return null
}

// data: { nodes: [{id, labels, properties}], rels: [{id, from, to, type, properties}] }
// dimension: 'nodeDegree' | 'retweet_count' (same value getNodeDimension() produces)
// directed: the old `arrows` flag — picks a directed vs undirected graph.
export function toGraphology(data, dimension, directed) {
  const graph = directed ? new MultiDirectedGraph() : new MultiGraph()
  const nodes = (data && data.nodes) || []
  const rels = (data && data.rels) || []

  // node size domain: scale across the dimension values actually present so one
  // huge nodeDegree doesn't dwarf everything (neovis auto-scaled; we replicate).
  const sizeVals = []
  for (const node of nodes) {
    const v = sizeablePropValue(node, dimension)
    if (v != null) sizeVals.push(v)
  }
  const [sMin, sMax] = minMax(sizeVals)

  for (const node of nodes) {
    if (graph.hasNode(node.id)) continue
    const raw = sizeablePropValue(node, dimension)
    const size = raw == null
      ? NODE_DEFAULT_SIZE
      : linearScale(raw, sMin, sMax, NODE_SIZE_RANGE[0], NODE_SIZE_RANGE[1])
    graph.addNode(node.id, {
      label: captionFor(node),
      size,
      color: colorFor(node),
      // placeholder coords; graphVisualization.js re-seeds with a circular layout
      // and ForceAtlas2 settles the final positions.
      x: Math.random(),
      y: Math.random(),
    })
  }

  // edge thickness domain
  const thickVals = []
  for (const rel of rels) {
    const v = num(rel.properties[REL_THICKNESS_BY_TYPE[rel.type]])
    if (v != null) thickVals.push(v)
  }
  const [tMin, tMax] = minMax(thickVals)

  for (const rel of rels) {
    if (!graph.hasNode(rel.from) || !graph.hasNode(rel.to)) continue
    if (graph.hasEdge(rel.id)) continue
    const prop = REL_THICKNESS_BY_TYPE[rel.type]
    const raw = prop != null ? num(rel.properties[prop]) : null
    const size = raw == null
      ? EDGE_DEFAULT_SIZE
      : linearScale(raw, tMin, tMax, EDGE_SIZE_RANGE[0], EDGE_SIZE_RANGE[1])
    graph.addEdgeWithKey(rel.id, rel.from, rel.to, { size, color: EDGE_COLOR })
  }

  return graph
}
