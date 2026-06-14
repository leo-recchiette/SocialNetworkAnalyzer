import { createElement, useEffect, useRef } from 'react'
import * as echarts from 'echarts'
import {
  Badge, Center, Divider, Group, Loader, Paper, Stack, Text,
} from '@mantine/core'
import { sna } from './bridge.js'
import { Hint } from '../components/DataPanel.jsx'

// Word-frequency .data panel, rendered with real Mantine. The legacy
// timelineVisualization.js drives it via renderWordFrequencyPanel(), which
// pushes the node into the React-owned panel (DataPanelHost) via sna.setDataPanel.

// Per-source field map for a single content occurrence. Mirrors the original
// visualizeSingleWord() markup (facebook / twitter / mbox).
function fieldsFor(sn, item) {
  const node = item.node || {}
  if (sn === 'facebook') {
    return [
      ['Content', node.content],
      ['Node degree', node.nodeDegree],
      ['Timestamp', node.timestamp],
      ['Dump profile', item.propertyDump],
    ]
  }
  if (sn === 'twitter') {
    return [
      ['Content', node.full_text],
      ['Node degree', node.nodeDegree],
      ['Timestamp', node.created_at],
      ['Dump profile', item.propertyDump],
    ]
  }
  // mbox (default)
  return [
    ['Sender', node.sender],
    ['To', node.to],
    ['Timestamp', node.time],
    ['Subject', node.subject],
    ['Content', node.content],
    ['Dump profile', item.propertyDump],
  ]
}

// timestamp field per source -> 'YYYY/MM'
function monthOf(sn, item) {
  const node = item.node || {}
  const ts = sn === 'twitter' ? node.created_at : sn === 'facebook' ? node.timestamp : node.time
  if (!ts) return null
  const parts = String(ts).split(' ')[0].split('/') // 'YYYY/MM/DD' -> [YYYY, MM, DD]
  return parts.length >= 2 ? parts[0] + '/' + parts[1] : null
}

// inclusive month sequence between two 'YYYY/MM' strings, so the trend line has
// a continuous x-axis (months with no occurrence show as 0, not a skipped gap).
function enumerateMonths(start, end) {
  const [sy, sm] = start.split('/').map(Number)
  const [ey, em] = end.split('/').map(Number)
  const out = []
  let y = sy
  let m = sm
  while (y < ey || (y === ey && m <= em)) {
    out.push(y + '/' + (m < 10 ? '0' + m : '' + m))
    m += 1
    if (m > 12) { m = 1; y += 1 }
  }
  return out
}

// occurrences of the selected word per month, derived from the fetched content
function buildTrend(sn, content) {
  const counts = {}
  for (const item of content) {
    const mth = monthOf(sn, item)
    if (mth) counts[mth] = (counts[mth] || 0) + 1
  }
  const present = Object.keys(counts).sort()
  if (present.length === 0) return { months: [], counts: [] }
  const months = enumerateMonths(present[0], present[present.length - 1])
  return { months, counts: months.map((m) => counts[m] || 0) }
}

// ECharts line chart of the word's monthly occurrence count (the temporal trend
// of the selected word). Rendered imperatively inside this React subtree.
function WordTrendChart({ months, counts }) {
  const ref = useRef(null)

  useEffect(() => {
    if (!ref.current) return undefined
    const chart = echarts.init(ref.current)
    chart.setOption({
      grid: { left: 8, right: 14, top: 18, bottom: 48, containLabel: true },
      tooltip: { trigger: 'axis', valueFormatter: (v) => v + ' mail' },
      xAxis: {
        type: 'category', data: months, boundaryGap: false,
        axisLabel: { rotate: 45, fontSize: 10, color: '#3f3f46' },
        axisLine: { lineStyle: { color: '#a1a1aa' } },
      },
      yAxis: {
        type: 'value', minInterval: 1,
        axisLabel: { color: '#3f3f46', fontSize: 10 },
        splitLine: { lineStyle: { color: '#e4e4e7' } },
      },
      series: [{
        type: 'line', data: counts, smooth: false,
        symbol: 'circle', symbolSize: 6,
        lineStyle: { color: '#cda730', width: 2 },
        itemStyle: { color: '#cda730' },
        areaStyle: { color: 'rgba(248,214,91,0.25)' },
      }],
    })
    const onResize = () => chart.resize()
    window.addEventListener('resize', onResize)
    return () => { window.removeEventListener('resize', onResize); chart.dispose() }
  }, [months.join('|'), counts.join('|')])

  return <div ref={ref} style={{ width: '100%', height: 170 }} />
}

function ContentCard({ sn, item }) {
  return (
    <Paper withBorder radius={0} p="xs" bg="#f4f4f5">
      <Stack gap={2}>
        {fieldsFor(sn, item).map(([label, value]) => (
          <Field key={label} label={label} value={value} />
        ))}
      </Stack>
    </Paper>
  )
}

function Field({ label, value }) {
  return (
    <div>
      <Text component="span" size="sm" fw={700} c="#18181b">{label}: </Text>
      <Text component="span" size="sm" c="#18181b" style={{ overflowWrap: 'break-word' }}>
        {value == null || value === '' ? '—' : String(value)}
      </Text>
    </div>
  )
}

function WordFrequencyPanel({ word, value, sn, content, loading }) {
  if (!word) return <Hint text="Try to select a word" />

  const trend = !loading && content && content.length > 0 ? buildTrend(sn, content) : null

  return (
    <Stack gap="sm">
      <Paper withBorder radius={0} p="xs" bg="#fafafa">
        <Text size="xs" tt="uppercase" fw={700} c="#71717a" mb={4}>You have selected</Text>
        <Group justify="space-between" wrap="nowrap" align="center">
          <Group gap="xs" wrap="nowrap">
            <Text size="sm" fw={700} c="#18181b">Word:</Text>
            <Text size="sm" c="#18181b">{word}</Text>
          </Group>
          <Badge color="yellow" radius={0} variant="filled">{value}%</Badge>
        </Group>
      </Paper>

      <Divider color="#3f3f46" />

      {loading ? (
        <Center py="md"><Loader color="yellow" size="sm" /></Center>
      ) : !content || content.length === 0 ? (
        <Text size="sm" c="#3f3f46" ta="center" py="xs">
          No content contains “{word}” in the selected range of time.
        </Text>
      ) : (
        <>
          {trend && trend.months.length > 0 && (
            <Paper withBorder radius={0} p="xs" bg="#fafafa">
              <Text size="xs" tt="uppercase" fw={700} c="#71717a" mb={4}>
                Trend over time — “{word}” ({content.length} mail)
              </Text>
              <WordTrendChart months={trend.months} counts={trend.counts} />
            </Paper>
          )}

          <Text size="sm" c="#18181b">
            The word <Text component="span" fw={700}>“{word}”</Text> is present in this content in
            the selected range of time:
          </Text>
          <Stack gap="xs">
            {content.map((item, i) => (
              <ContentCard key={i} sn={sn} item={item} />
            ))}
          </Stack>
        </>
      )}
    </Stack>
  )
}

export function renderWordFrequencyPanel(props) {
  sna.setDataPanel(createElement(WordFrequencyPanel, props))
}
