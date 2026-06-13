import $ from 'jquery'
import * as echarts from 'echarts'
import { sna } from './bridge.js'
import { noDataFoundVisualization, showDataSpinner } from './dom.js'
import { visualizeSingleWord } from './dataVisualization.js'

// Word-frequency visualization. Replaces the old frappe-gantt timeline with an
// ECharts heatmap (x = month, y = word, color = frequency), which fits
// "word frequency over time" far better than a gantt chart. The backend contract
// is unchanged: getTimelineObject.py returns [{timestamp:'YYYY/MM', word, value}]
// and clicking a cell still calls getSingleWordsFrequencyContent.py.

let chart = null

function onResize() {
  if (chart) chart.resize()
}

function disposeChart() {
  if (chart) {
    try { chart.dispose() } catch (e) { /* already disposed */ }
    chart = null
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
        $('.data').html(
          '<div class="data-item">' +
          '<span> Try to select a word </span>' +
          '</div>'
        )
        buildHeatmap(data)
      } else {
        noDataFoundVisualization()
      }
    },
    error: function () {
      console.log('No word')
    }
  })
}

function buildHeatmap(data) {
  disposeChart()
  $('.content').html('<div id="chart" style="height: 100%; width: 100%"></div>')

  const rows = data.filter(function (d) { return d.word && d.word !== '' })

  // Build the month (x) and word (y) axes and the [xIndex, yIndex, value] points.
  // Rows arrive ordered by timestamp (ORDER BY in getTimelineObject.py), and
  // 'YYYY/MM' strings sort chronologically, so insertion order is correct.
  const months = []
  const monthIndex = {}
  const words = []
  const wordIndex = {}
  const points = []
  let maxVal = 0

  for (const r of rows) {
    const m = r.timestamp
    const w = r.word
    if (!(m in monthIndex)) { monthIndex[m] = months.length; months.push(m) }
    if (!(w in wordIndex)) { wordIndex[w] = words.length; words.push(w) }
    const v = parseFloat(r.floatVal != null ? r.floatVal : r.value) || 0
    if (v > maxVal) maxVal = v
    points.push([monthIndex[m], wordIndex[w], v])
  }

  chart = echarts.init(document.getElementById('chart'))
  chart.setOption({
    tooltip: {
      position: 'top',
      formatter: function (p) {
        return words[p.data[1]] + ' — ' + months[p.data[0]] + ': ' + p.data[2]
      }
    },
    grid: { left: 24, right: 36, top: 24, bottom: 90, containLabel: true },
    xAxis: { type: 'category', data: months, splitArea: { show: true }, axisLabel: { rotate: 45 } },
    yAxis: { type: 'category', data: words, splitArea: { show: true } },
    visualMap: {
      min: 0,
      max: maxVal || 1,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 12,
    },
    // Many words make the y-axis very tall; let the user scroll/zoom through them.
    dataZoom: [
      { type: 'slider', yAxisIndex: 0, filterMode: 'none', width: 14, right: 6 },
      { type: 'inside', yAxisIndex: 0, filterMode: 'none' },
    ],
    series: [{
      type: 'heatmap',
      data: points,
      label: { show: false },
      emphasis: { itemStyle: { shadowBlur: 6, shadowColor: 'rgba(0,0,0,0.3)' } },
    }],
  })

  chart.on('click', function (params) {
    if (!params.data) return
    const word = words[params.data[1]]
    const value = params.data[2]
    // Reuse the existing single-word flow; it reads task.name and task.progress.
    showSingleTask({ name: word, progress: value }, sna.dataToSearch)
  })

  window.addEventListener('resize', onResize)
}

function showSingleTask (task, dataToSearch)
{
    sna.setDataViz1('selected');

    $('.data').html(
        '<div class="data-item ">' +
        '<p class=\'dataHeader\'>You have selected </p>' +
        '<span class=\'dataKey\'>Word: </span>' +
        '<span class=\'dataValue\'>' + task.name + '</span>' +
        '<br>' +
        '<span class=\'dataKey\'>Percentage: </span>' +
        '<span class=\'dataValue\'>' + task.progress + '%</span>' +
        '<br>' +
        '</div>' +
        '<hr>'
    );

    let action = 'getSingleWordsFrequencyContent';

     let dts = JSON.parse(dataToSearch);

     let sn = dts['sn'];

      dataToSearch = JSON.stringify(dts);

    let word = task.name;
    $.ajax({
        url: 'server.php',
        dataType: 'JSON',
        data: {action, word, dataToSearch},
        type: 'post',
        success:function (data){
            visualizeSingleWord(data, sn, word)
        }
    });


}

export { getWords }
