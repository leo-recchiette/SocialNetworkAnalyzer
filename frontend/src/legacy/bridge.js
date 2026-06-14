// Shared mutable state between the React app and the legacy (jQuery-based)
// visualization modules. React keeps every field in sync on each render and
// installs the setDataViz callbacks; the legacy modules only read fields and
// invoke the callbacks - they never touch React state directly.
export const sna = {
  // current search context (mirrors React state)
  dataToSearch: '',
  usr: '',
  sn: 'mbox',
  dataViz1: 'selected',
  dataViz2: 'contacts',

  // graph filter radios (mirrors React state, read by allQueries.js)
  fbUserType: 'All',
  fbNodeType: 'all',
  fbMap: 'all',
  twUserType: 'All',
  tweetType: 'all',
  twNodeType: 'nodeDegree',

  // installed by React: switch the data panel tabs from legacy code
  setDataViz1: () => {},
  setDataViz2: () => {},

  // installed by DataPanelHost: render a React node into the (light) .data
  // island. Legacy modules build the node and push it here instead of writing
  // HTML into .data, so the panel stays inside the main React tree.
  setDataPanel: () => {},
}