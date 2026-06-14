import $ from 'jquery'
import { createElement } from 'react'
import { sna } from './bridge.js'
import { Hint, Spinner, NoData } from '../components/DataPanel.jsx'

// Helpers around the two imperative containers (.content and .data). The .data
// panel is React-owned (DataPanelHost): these helpers push its shared states
// through sna.setDataPanel as real Mantine. .content is still plain jQuery (it
// hosts the Sigma/OpenLayers/ECharts canvases).

export function clearDataSpace() {
  sna.setDataPanel(null)
}

export function clearContentSpace() {
  $('.content').html('')
}

export function showDataSpinner() {
  sna.setDataPanel(createElement(Spinner))
}

export function showDataHint(text) {
  sna.setDataPanel(createElement(Hint, { text }))
}

export function noDataFoundVisualization() {
  sna.setDataPanel(createElement(NoData))
}
