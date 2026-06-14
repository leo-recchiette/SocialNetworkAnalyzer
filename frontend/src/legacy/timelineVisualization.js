import $ from 'jquery'
import * as echarts from 'echarts'
import { sna } from './bridge.js'
import { noDataFoundVisualization, showDataSpinner } from './dom.js'
import { renderWordFrequencyPanel } from './wordFrequencyPanel.jsx'

// Word-frequency visualization. Replaces the old frappe-gantt timeline with an
// ECharts heatmap (x = month, y = word, color = frequency), which fits
// "word frequency over time" far better than a gantt chart. The backend contract
// is unchanged: getTimelineObject.py returns [{timestamp:'YYYY/MM', word, value}]
// and clicking a cell still calls getSingleWordsFrequencyContent.py.

let chart = null
let resizeObserver = null

function onResize() {
  if (chart) chart.resize()
}

function disposeChart() {
  if (chart) {
    try { chart.dispose() } catch (e) { /* already disposed */ }
    chart = null
  }
  if (resizeObserver) {
    try { resizeObserver.disconnect() } catch (e) { /* noop */ }
    resizeObserver = null
  }
  window.removeEventListener('resize', onResize)
}

function getWords(dataToSearch) {
  let action = 'getTimelineObject'

  $.ajax({
    url: 'server.php',
    dataType: 'JSON',
    data: { dataToSearch, action },
    type: 'post',
    beforeSend: function () {
      showDataSpinner()
    },
    success: function (data) {
      if (data.length > 0) {
        renderWordFrequencyPanel({ word: null })
        buildHeatmap(data)
      } else {
        noDataFoundVisualization()
      }
    },
    // Without this the spinner (shown in beforeSend) spins forever on failure.
    // server.php runs the Python with 2>&1, so responseText usually carries the
    // traceback — log it to diagnose backend word-frequency errors.
    error: function (xhr) {
      console.error('getTimelineObject failed:', xhr && xhr.responseText)
      noDataFoundVisualization()
    }
  })
}

// How many of the highest-scoring words to keep, and how many rows to show in
// the initial scroll window. The full word list is a long tail of low-relevance
// terms that turns the y-axis into an unreadable wall of 1px rows.
const TOP_WORDS = 100
const VISIBLE_ROWS = 30

function buildHeatmap(data) {
  disposeChart()
  $('.content').html('<div id="chart" style="height: 100%; width: 100%"></div>')

  const rows = data.filter(function (d) { return d.word && d.word !== '' })

  // value/floatVal is the word's TF-IDF score (constant per word across months).
  // It drives word RANKING (keep the most relevant TOP_WORDS) and the % badge in
  // the detail panel. The per-month occurrence COUNT (below) drives cell colour.
  const wordVal = {}
  for (const r of rows) {
    const v = parseFloat(r.floatVal != null ? r.floatVal : r.value) || 0
    if (!(r.word in wordVal) || v > wordVal[r.word]) wordVal[r.word] = v
  }
  const totalWords = Object.keys(wordVal).length
  // Keep the TOP_WORDS most relevant (drops the noisy long tail), then display
  // them ALPHABETICALLY. Sorted descending (z..a) so 'a' lands at the last index,
  // which ECharts renders at the TOP of a (non-inverse) category axis.
  const words = Object.keys(wordVal)
    .sort(function (a, b) { return wordVal[b] - wordVal[a] })
    .slice(0, TOP_WORDS)
    .sort()
    .reverse()
  const wordIndex = {}
  words.forEach(function (w, i) { wordIndex[w] = i })

  // months on the x-axis, in chronological order (rows arrive ORDER BY timestamp,
  // and 'YYYY/MM' strings sort chronologically, so first-seen order is correct).
  const months = []
  const monthIndex = {}
  for (const r of rows) {
    if (!(r.timestamp in monthIndex)) { monthIndex[r.timestamp] = months.length; months.push(r.timestamp) }
  }

  // Cell colour = per-month occurrence COUNT (countVal), so the intensity varies
  // along a word's row over time (same metric as the per-word trend chart). Falls
  // back to the relevance value if an older backend doesn't send counts yet.
  const points = []
  let minVal = Infinity
  let maxVal = 0
  for (const r of rows) {
    if (!(r.word in wordIndex)) continue
    const c = parseFloat(
      r.countVal != null ? r.countVal
        : r.count != null ? r.count
          : r.floatVal != null ? r.floatVal : r.value
    ) || 0
    if (c > maxVal) maxVal = c
    if (c < minVal) minVal = c
    points.push([monthIndex[r.timestamp], wordIndex[r.word], c])
  }
  if (!isFinite(minVal)) minVal = 0

  // initial vertical window: show the top VISIBLE_ROWS (highest-scoring) words
  const yStart = words.length > VISIBLE_ROWS ? ((words.length - VISIBLE_ROWS) / words.length) * 100 : 0

  chart = echarts.init(document.getElementById('chart'))
  chart.setOption({
    backgroundColor: '#fafafa',
    title: totalWords > words.length ? {
      text: 'Top ' + words.length + ' of ' + totalWords + ' words by relevance (A–Z)',
      left: 8, top: 2,
      textStyle: { fontSize: 11, fontWeight: 'normal', color: '#71717a' },
    } : undefined,
    tooltip: {
      position: 'top',
      formatter: function (p) {
        return words[p.data[1]] + ' — ' + months[p.data[0]] + ': ' + p.data[2] + ' occurrences'
      }
    },
    grid: { left: 8, right: 56, top: 28, bottom: 92, containLabel: true },
    xAxis: {
      type: 'category', data: months,
      axisLabel: { rotate: 45, color: '#3f3f46', fontSize: 11 },
      axisLine: { lineStyle: { color: '#a1a1aa' } },
      splitArea: { show: false },
    },
    yAxis: {
      type: 'category', data: words,
      axisLabel: { color: '#18181b', fontSize: 11 },
      axisLine: { lineStyle: { color: '#a1a1aa' } },
      splitArea: { show: false },
    },
    visualMap: {
      min: minVal,
      max: maxVal || 1,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 12,
      text: ['high', 'low'],
      textStyle: { color: '#3f3f46' },
      // amber ramp with a clearly-visible floor (#fde68a, distinct from the
      // light canvas) up to a dark ceiling, so even low scores read as a cell.
      inRange: { color: ['#fde68a', '#fbbf24', '#f59e0b', '#d97706', '#9a3412'] },
    },
    // Top-100 words still overflow vertically; window to VISIBLE_ROWS and let
    // the user scroll/zoom (slider on the right + wheel inside the plot).
    dataZoom: [
      { type: 'slider', yAxisIndex: 0, filterMode: 'none', width: 14, right: 8, start: yStart, end: 100, brushSelect: false },
      { type: 'inside', yAxisIndex: 0, filterMode: 'none', start: yStart, end: 100 },
    ],
    series: [{
      type: 'heatmap',
      data: points,
      label: { show: false },
      // gaps between cells (border = canvas color) make the grid legible
      itemStyle: { borderColor: '#fafafa', borderWidth: 1 },
      emphasis: { itemStyle: { borderColor: '#18181b', borderWidth: 1, shadowBlur: 4, shadowColor: 'rgba(0,0,0,0.3)' } },
    }],
  })

  chart.on('click', function (params) {
    if (!params.data) return
    const word = words[params.data[1]]
    // Pass the word's TF-IDF relevance (not the clicked cell's month count) so the
    // detail panel's % badge stays a relevance score; the trend chart shows counts.
    showSingleTask({ name: word, progress: wordVal[word] }, sna.dataToSearch)
  })

  // Fill all available height: the flex container's final size isn't always
  // settled at init time and it changes when the drawer/filters toggle, so keep
  // the canvas matched to the container instead of only reacting to window resize.
  const el = document.getElementById('chart')
  if (el && typeof ResizeObserver !== 'undefined') {
    resizeObserver = new ResizeObserver(function () { if (chart) chart.resize() })
    resizeObserver.observe(el)
  }
  window.addEventListener('resize', onResize)
}

function showSingleTask (task, dataToSearch)
{
    sna.setDataViz1('selected');

    const dts = JSON.parse(dataToSearch);
    const sn = dts['sn'];
    const word = task.name;

    // show the selected word immediately, with the content list loading
    renderWordFrequencyPanel({ word, value: task.progress, sn, content: null, loading: true });

    $.ajax({
        url: 'server.php',
        dataType: 'JSON',
        data: { action: 'getSingleWordsFrequencyContent', word, dataToSearch: JSON.stringify(dts) },
        type: 'post',
        success: function (data) {
            renderWordFrequencyPanel({ word, value: task.progress, sn, content: data, loading: false });
        },
        error: function () {
            renderWordFrequencyPanel({ word, value: task.progress, sn, content: [], loading: false });
        }
    });
}

export { getWords }
