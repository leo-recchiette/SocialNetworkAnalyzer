import { createElement } from 'react'
import { sna } from './bridge.js'
import { noDataFoundVisualization } from './dom.js'
import { DataPanel } from '../components/DataPanel.jsx'

// Builds a plain-object `model` from the server response for the current
// (socialNetwork × graphType × dataViz2) combination and renders it as real
// Mantine components via DataPanel. Replaces the old jQuery string-concatenated
// markup; the fields shown per source are kept identical to the original.
//
// Reachability note: the data-panel tabs (MainSection.jsx) only enable
// dataViz2='links' for relNet, and 'contacts' stays the value for map/wordFrec.
// So the original trafficNet/map "links" branches (several referenced functions
// that were never even defined) were dead; here links are handled for relNet
// only and other link views fall through to "no data".

function render(model) {
  if (!model) return noDataFoundVisualization()
  sna.setDataPanel(createElement(DataPanel, { model }))
}

function dataVisualization(data) {
  const dts = JSON.parse(sna.dataToSearch)

  if (!(data.length > 0)) return noDataFoundVisualization()

  // A response carrying a Counter is the "selected" view before anything is
  // picked: 0 means nothing matched, otherwise prompt the user to select.
  if ('Counter' in data[0]) {
    if (data[0]['Counter'] == 0) return noDataFoundVisualization()
    const what = sna.dataViz2 === 'links' ? 'link' : 'node'
    return render({ kind: 'placeholder', text: `Try to select a ${what}` })
  }

  const sn = dts['sn']
  const gt = dts['graphType']
  const isContacts = dts['dataViz2'] === 'contacts'

  let model = null
  if (sn === 'facebook') model = isContacts ? facebookContacts(data, gt, dts) : linksFor(data, gt)
  else if (sn === 'twitter') model = isContacts ? twitterContacts(data, gt, dts) : linksFor(data, gt)
  else if (sn === 'mbox') model = isContacts ? mboxContacts(data, gt, dts) : linksFor(data, gt)

  render(model)
}

/* ---- shared builders ---- */

// Tagged-together table (relNet links, all sources). Other link views are
// unreachable from the UI, so they fall through to null -> "no data".
function linksFor(data, graphType) {
  if (graphType !== 'relNet') return null
  return { kind: 'links', rows: data.map((d) => ({ name1: d['name_1'], name2: d['name_2'], link: d['link'] })) }
}

function wordsModel(data, dts) {
  const dv = dts['dataViz1']
  let title = null
  if (dv === 'filtered') title = 'Relevant words in the selected range of time'
  else if (dv === 'all') title = 'All time Relevant words'
  return { kind: 'words', title, rows: data.map((d) => ({ word: d['word'], value: d['value'] })) }
}

/**********************  FACEBOOK **********************/

function facebookContacts(data, graphType, dts) {
  if (graphType === 'relNet') return facebookContactsRel(data)
  if (graphType === 'trafficNet') return facebookContactsTraffic(data)
  if (graphType === 'map') return facebookContactsMap(data)
  return wordsModel(data, dts)
}

function facebookContactsRel(data) {
  const records = data.map((d) => {
    const n = d['node']
    const fields = [
      { label: 'Name', value: n['name'] },
      { label: 'Node degree', value: n['nodeDegree'], mono: true },
      { label: 'Tagged together count', value: d['taggedTogetherValue'], mono: true },
      { label: 'Dump profile', value: d['propertyDump'] },
    ]
    if ('removed_timestamp' in n) fields.push({ label: 'Removed timestamp', value: n['removed_timestamp'], mono: true })
    else fields.push({ label: 'Timestamp', value: n['timestamp'], mono: true })

    const lists = []
    if ('phoneContacts' in n) lists.push({ label: 'Contacts', items: n['phoneContacts'] })
    return { fields, lists }
  })

  // taggedWith comes from data[0] in the original; show it on the first record.
  if (records[0] && 'taggedWith' in data[0] && data[0]['taggedWith'].length > 0)
    records[0].spoiler = { label: 'click to show people tagged in this content', items: data[0]['taggedWith'] }

  return { kind: 'records', records }
}

function facebookContactsTraffic(data) {
  if (sna.dataViz1 === 'selected') {
    if ('node' in data[0]) {
      const d = data[0]
      const n = d['node']
      const rec = {
        fields: [
          { label: 'Content', value: n['content'] },
          { label: 'Node degree', value: d['nodeDegree'], mono: true },
          { label: 'Timestamp', value: n['timestamp'], mono: true },
          { label: 'Dump profile', value: d['propertyDump'] },
        ],
      }
      if (d['taggedWith'] && d['taggedWith'].length > 0)
        rec.spoiler = { label: 'click to show people tagged in this content', items: d['taggedWith'] }
      return { kind: 'records', records: [rec] }
    }
    if ('StartOfConversation' in data[0]) {
      const soc = data[0]['StartOfConversation']
      const records = [{
        lists: [{ label: 'Participants', items: soc['participants'] }],
        fields: [
          { label: 'Dump profile', value: data[0]['propertyDump'] },
          { label: 'Node degree', value: soc['nodeDegree'], mono: true },
        ],
      }]
      // the conversation thread: start message, then each reply
      records.push({
        fields: [
          { label: 'Sender', value: soc['sender'] },
          { label: 'Timestamp', value: soc['timestamp'], mono: true },
          { label: 'Content', value: soc['content'] },
        ],
      })
      for (let i = 1; i < data.length; i++) {
        const r = data[i]['Replay']
        records.push({
          fields: [
            { label: 'Sender', value: r['sender'] },
            { label: 'Timestamp', value: r['timestamp'], mono: true },
            { label: 'Content', value: r['content'] },
          ],
        })
      }
      return { kind: 'records', records }
    }
    return null
  }

  // filtered / all
  const records = data.map((d) => {
    const n = d['node']
    const rec = {
      fields: [
        { label: 'Content', value: n['content'] },
        { label: 'Node degree', value: n['nodeDegree'], mono: true },
        { label: 'Timestamp', value: n['timestamp'], mono: true },
        { label: 'Dump profile', value: d['propertyDump'] },
      ],
      lists: [],
    }
    if ('participants' in n) rec.lists.push({ label: 'Participants', items: n['participants'] })
    if (d['taggedWith'] && d['taggedWith'].length > 0)
      rec.spoiler = { label: 'click to show people tagged in this content', items: d['taggedWith'] }
    return rec
  })
  return { kind: 'records', records }
}

function facebookContactsMap(data) {
  const records = data.map((d) => {
    const p = d['place']
    if ('content' in p) {
      return {
        fields: [
          { label: 'Content', value: p['content'] },
          { label: 'Node degree', value: p['nodeDegree'], mono: true },
          { label: 'Timestamp', value: p['timestamp'], mono: true },
          { label: 'Place name', value: p['place_name'] },
          { label: 'Dump profile', value: data[0]['propertyDump'] },
        ],
      }
    }
    return {
      fields: [
        { label: 'Name', value: p['name'] },
        { label: 'Latitude', value: p['place_latitude'], mono: true },
        { label: 'Longitude', value: p['place_longitude'], mono: true },
        { label: 'Timestamp', value: p['timestamp'], mono: true },
        { label: 'Dump profile', value: data[0]['propertyDump'] },
      ],
    }
  })
  return { kind: 'records', records }
}

/**********************  TWITTER  **********************/

function twitterContacts(data, graphType, dts) {
  if (graphType === 'relNet') return twitterContactsRel(data)
  if (graphType === 'trafficNet') return twitterContactsTraffic(data)
  if (graphType === 'map') return twitterContactsMap(data)
  return wordsModel(data, dts)
}

function twitterContactsRel(data) {
  const records = data.map((d) => {
    const n = d['node']
    return {
      fields: [
        { label: 'Name', value: n['name'] },
        { label: 'Account name', value: n['screen_name'] },
        { label: 'Twitter profile', href: n['user_link'] },
        { label: 'Node degree', value: n['nodeDegree'], mono: true },
        { label: 'Tagged together count', value: d['taggedTogetherValue'], mono: true },
        { label: 'Dump profile', value: d['propertyDump'] },
      ],
    }
  })
  if (records[0] && 'taggedWith' in data[0] && data[0]['taggedWith'].length > 0)
    records[0].spoiler = { label: 'click to show people tagged in this tweet', items: data[0]['taggedWith'] }
  return { kind: 'records', records }
}

function twitterContactsTraffic(data) {
  const records = data.map((d) => {
    const n = d['node']
    const rec = {
      fields: [
        { label: 'Content', value: n['full_text'] },
        { label: 'Timestamp', value: n['created_at'], mono: true },
        { label: 'Node degree', value: d['nodeDegree'], mono: true },
        { label: 'Dump profile', value: d['propertyDump'] },
      ],
    }
    if (n['hashtags_text'] !== '') rec.fields.push({ label: 'Hashtags text', value: n['hashtags_text'] })
    if (d['taggedWith'] && d['taggedWith'].length > 0)
      rec.spoiler = { label: 'click to show people tagged in this tweet', items: d['taggedWith'] }
    return rec
  })
  return { kind: 'records', records }
}

function twitterContactsMap(data) {
  const records = data.map((d) => {
    const p = d['place']
    const fields = [
      { label: 'Content', value: p['full_text'] },
      { label: 'Timestamp', value: p['created_at'], mono: true },
      { label: 'Latitude', value: p['latitude'], mono: true },
      { label: 'Longitude', value: p['longitude'], mono: true },
      { label: 'Retweet count', value: p['retweet_count'], mono: true },
      { label: 'Node degree', value: p['nodeDegree'], mono: true },
      { label: 'Dump profile', value: d['propertyDump'] },
    ]
    if ('url' in p) fields.push({ label: 'External content', href: p['url'] })
    if ('hashtags_text' in p && p['hashtags_text'] !== '#') fields.push({ label: 'Hashtags', value: p['hashtags_text'] })
    return { fields }
  })
  return { kind: 'records', records }
}

/**********************  MBOX  **********************/

function mboxContacts(data, graphType, dts) {
  // relNet and trafficNet render identically in the original.
  if (graphType === 'relNet' || graphType === 'trafficNet') return mboxContactsNet(data)
  if (graphType === 'map') return null
  return wordsModel(data, dts)
}

function mboxContactsNet(data) {
  const records = data.map((d) => {
    const n = d['node']
    return {
      fields: [
        { label: 'Name', value: n['label'] },
        { label: 'Node degree', value: n['nodeDegree'], mono: true },
        { label: 'Tagged together count', value: d['taggedTogetherValue'], mono: true },
        { label: 'Dump profile', value: data[0]['node']['userProfileProperty'] },
      ],
    }
  })
  if (records[0] && 'taggedWith' in data[0] && data[0]['taggedWith'].length > 0)
    records[0].spoiler = { label: 'click to show people tagged whit this person', items: data[0]['taggedWith'] }
  return { kind: 'records', records }
}

export { dataVisualization }
