import { useEffect, useRef, useState } from 'react'
import $ from 'jquery'
import { Burger, Group, Title } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'

import SideDrawer from './components/SideDrawer.jsx'
import HelpModal from './components/HelpModal.jsx'
import FiltersMenu from './components/FiltersMenu.jsx'
import MainSection from './components/MainSection.jsx'

import { sna } from './legacy/bridge.js'
import { clearDataSpace, clearContentSpace, noDataFoundVisualization, showDataSpinner } from './legacy/dom.js'
import { createQueryForDrawing } from './legacy/allQueries.js'
import { drawGraph, getNodeDimension, stabilizeGraph } from './legacy/graphVisualization.js'
import { dataVisualization } from './legacy/dataVisualization.js'
import { createWorldMap } from './legacy/mapVisualization.js'
import { getWords } from './legacy/timelineVisualization.js'
import { getTodayDate, validateEmail, dataToSearchJSONCreator, epochToDateLabel } from './utils.js'

const DAY = 86400
const epoch = (s) => new Date(s).getTime() / 1000

export default function App() {
  // ---- auth ----
  const [usr, setUsr] = useState('')
  const [drawerOpened, drawer] = useDisclosure(false)
  const [helpOpened, help] = useDisclosure(true) // the old app opened the help modal on load

  // ---- search parameters ----
  const [sn, setSn] = useState('facebook')
  const [keyword, setKeyword] = useState('')
  const [person, setPerson] = useState('')
  const [nodeVal, setNodeVal] = useState(1)
  const [nodeMax, setNodeMax] = useState(50)
  const [edgeVal, setEdgeVal] = useState(1)
  const [edgeMax, setEdgeMax] = useState(50)
  const [dateBounds, setDateBounds] = useState([epoch('2000.01.01'), epoch(getTodayDate())])
  const [dateRange, setDateRange] = useState([epoch('2020.01.01'), epoch('2020.12.13')])
  const [graphType, setGraphType] = useState('relNet')
  const [dataViz1, setDataViz1] = useState('selected')
  const [dataViz2, setDataViz2] = useState('contacts')
  const [sortValue, setSortValue] = useState('timedesc')

  // ---- graph filter radios ----
  const [fbUserType, setFbUserType] = useState('All')
  const [fbNodeType, setFbNodeType] = useState('all')
  const [fbMap, setFbMap] = useState('all')
  const [twUserType, setTwUserType] = useState('All')
  const [tweetType, setTweetType] = useState('all')
  const [twNodeType, setTwNodeType] = useState('nodeDegree')

  // ---- transient UI feedback ----
  const [loginFeedback, setLoginFeedback] = useState({ field: null, msg: null })
  const [registerBtn, setRegisterBtn] = useState({ color: null, label: 'Register' })
  const [searchBtn, setSearchBtn] = useState({ color: null, label: 'Search' })
  const [changeMailBtn, setChangeMailBtn] = useState({ color: null, label: 'Change' })
  const [changePassBtn, setChangePassBtn] = useState({ color: null, label: 'Change' })
  const [deleteFeedback, setDeleteFeedback] = useState(null)
  const [upload, setUpload] = useState({
    visible: false, progress: null, msg: '', msgColor: 'gray', btnColor: null, btnLabel: 'Upload file',
  })

  // Everything setEnvironment needs, always fresh (avoids stale closures).
  const paramsRef = useRef({})
  paramsRef.current = {
    usr, sn, keyword, person, nodeVal, edgeVal, dateRange, graphType,
    dataViz1, dataViz2, sortValue,
    fbUserType, fbNodeType, fbMap, twUserType, tweetType, twNodeType,
  }

  function syncSna(s) {
    Object.assign(sna, {
      usr: s.usr, sn: s.sn, dataViz1: s.dataViz1, dataViz2: s.dataViz2,
      fbUserType: s.fbUserType, fbNodeType: s.fbNodeType, fbMap: s.fbMap,
      twUserType: s.twUserType, tweetType: s.tweetType, twNodeType: s.twNodeType,
    })
  }

  // keep the bridge in sync and install the callbacks used by the legacy modules
  useEffect(() => {
    syncSna(paramsRef.current)
  })
  useEffect(() => {
    sna.setDataViz1 = (v) => setDataViz1(v)
    sna.setDataViz2 = (v) => setDataViz2(v)
  }, [])

  function getNodeToDisplay(gt, social, s) {
    if (gt === 'relNet') {
      if (social === 'facebook') return s.fbUserType
      if (social === 'twitter') return s.twUserType
    } else if (gt === 'trafficNet') {
      if (social === 'facebook') return s.fbNodeType
      if (social === 'twitter') return s.tweetType
    } else if (gt === 'map') {
      if (social === 'facebook') return s.fbMap
    }
    return ''
  }

  function getDataAjax(ntd) {
    $.ajax({
      url: 'server.php',
      dataType: 'json',
      data: { dataToSearch: sna.dataToSearch, action: 'getData', ntd },
      type: 'post',
      beforeSend: showDataSpinner,
      success: (data) => dataVisualization(data),
      error: () => console.log('errore'),
    })
  }

  // ---- the heart of the old main.js, ported ----
  function setEnvironment(overrides = {}) {
    const s = { ...paramsRef.current, ...overrides }

    clearDataSpace()

    if (s.usr === '') return

    syncSna(s)

    const start_date = epochToDateLabel(s.dateRange[0])
    const end_date = epochToDateLabel(s.dateRange[1])

    const { cmd, direction } = createQueryForDrawing(
      s.keyword, s.person, start_date, end_date, s.nodeVal, s.edgeVal, s.sn, s.usr, s.graphType)

    sna.dataToSearch = dataToSearchJSONCreator(
      s.keyword, s.person, start_date, end_date, s.nodeVal, s.edgeVal,
      s.sn, s.usr, s.graphType, 'selected', 'contacts', s.sortValue)

    const dimension = getNodeDimension(s.sn, s.graphType)
    const ntd = getNodeToDisplay(s.graphType, s.sn, s)

    setDataViz1('selected')
    setDataViz2('contacts')
    sna.dataViz1 = 'selected'
    sna.dataViz2 = 'contacts'

    if (s.graphType === 'relNet' || s.graphType === 'trafficNet') {
      drawGraph(cmd, direction, dimension)
    } else if (s.graphType === 'map') {
      clearContentSpace()
      const markersToDisplay = s.sn === 'facebook' ? s.fbMap : ''

      $.ajax({
        url: 'server.php',
        dataType: 'json',
        data: { dataToSearch: sna.dataToSearch, action: 'getMarker', markersToDisplay },
        type: 'post',
        success: (data) => createWorldMap(data),
        error: () => {
          sna.dataToSearch = ''
          noDataFoundVisualization()
        },
      })
    } else if (s.graphType === 'wordFrec') {
      clearContentSpace()
      getWords(sna.dataToSearch)
    }

    if (s.graphType !== 'wordFrec') getDataAjax(ntd)
  }

  function setSliders(usrArg, snArg) {
    $.ajax({
      url: 'server.php',
      dataType: 'json',
      data: { usr: usrArg, sn: snArg },
      type: 'post',
      success: (data) => {
        const min = epoch(data[0])
        const max = epoch(data[1])
        const start = min
        const end = max

        setNodeVal(0); setNodeMax(data[2])
        setEdgeVal(0); setEdgeMax(data[3])
        setDateBounds([min, max])
        setDateRange([start, end])

        setEnvironment({ usr: usrArg, sn: snArg, nodeVal: 0, edgeVal: 0, dateRange: [start, end] })
      },
      error: () => {
        sna.dataToSearch = ''
        noDataFoundVisualization()
      },
    })
  }

  // ---- auth ----
  function login(mail, pass) {
    $.ajax({
      url: 'server.php',
      dataType: 'json',
      cache: false,
      data: { user: mail, pass, action: 'login' },
      type: 'post',
      success: (data) => {
        if (data['value'] === 1) {
          const u = data['user_mail']
          setUsr(u)
          setSliders(u, paramsRef.current.sn)
        } else if (data['value'] === -1) {
          setLoginFeedback({ field: 'password', msg: 'Wrong password' })
          setTimeout(() => setLoginFeedback({ field: null, msg: null }), 3000)
        } else if (data['value'] === 0) {
          setLoginFeedback({ field: 'mail', msg: data['user_mail'] })
          setTimeout(() => setLoginFeedback({ field: null, msg: null }), 3000)
        }
      },
      error: () => console.log("that's something wrong. Please try again"),
    })
  }

  function flashRegister(color, label) {
    setRegisterBtn({ color, label })
    setTimeout(() => setRegisterBtn({ color: null, label: 'Register' }), 3000)
  }

  function register(mail, pass) {
    if (!validateEmail(mail)) return flashRegister('red', 'Insert a valid email')
    if (pass === '') return flashRegister('red', 'Insert a valid password')

    $.ajax({
      url: 'server.php',
      dataType: 'json',
      cache: false,
      data: { user: mail, pass, action: 'register' },
      type: 'post',
      success: (data) => {
        if (data['value'] === 1) flashRegister('orange', data['user_mail'])
        else if (data['value'] === 0) flashRegister('green', data['user_mail'])
      },
      error: () => console.log("that's something wrong. Please try again"),
    })
  }

  function logout() {
    setUsr('')
    sna.dataToSearch = ''
    clearContentSpace()
    clearDataSpace()
  }

  // ---- dumps ----
  function uploadDump(file, wordFrecOption) {
    const fail = (msg) => {
      clearContentSpace()
      clearDataSpace()
      setUpload((u) => ({ ...u, btnColor: 'red', btnLabel: msg }))
      setTimeout(() => setUpload((u) => ({ ...u, btnColor: null, btnLabel: 'Upload file', msg: '' })), 3000)
    }

    if (!file) return fail('Please select a file')
    const extension = file.name.split('.').pop().toLowerCase()
    if ($.inArray(extension, ['zip', 'mbox']) === -1)
      return fail('This extension is not allowed. Please select a correct file')

    const fd = new FormData()
    fd.append('file', file)
    // consistency checks made server side
    fd.append('user', paramsRef.current.usr)
    fd.append('wordFrecOption', wordFrecOption)

    $.ajax({
      url: 'server.php',
      dataType: 'text',
      cache: false,
      contentType: false,
      processData: false,
      data: fd,
      type: 'post',
      xhr: function () {
        const xhr = new window.XMLHttpRequest()
        xhr.upload.addEventListener('progress', (evt) => {
          if (evt.lengthComputable) {
            const percentComplete = Math.round((evt.loaded / evt.total) * 100)
            setUpload((u) => ({ ...u, visible: true, progress: percentComplete }))
            if (percentComplete >= 100)
              setUpload((u) => ({
                ...u, msg: 'Upload done. Waiting while data is processed', msgColor: 'gray',
              }))
          }
        }, false)
        return xhr
      },
      beforeSend: () => setUpload((u) => ({ ...u, visible: true, progress: 0, msg: '' })),
      success: (php_script_response) => {
        setSliders(paramsRef.current.usr, paramsRef.current.sn)
        console.log(php_script_response)
        clearContentSpace()
        clearDataSpace()
        setUpload((u) => ({ ...u, progress: null, msg: php_script_response, msgColor: 'green' }))
        setTimeout(() => setUpload((u) => ({ ...u, visible: false, msg: '' })), 6000)
      },
    })
  }

  function deleteDump(valueToDelete) {
    $.ajax({
      url: 'server.php',
      dataType: 'text',
      cache: false,
      data: { usr: paramsRef.current.usr, valueToDelete },
      type: 'post',
      success: (data) => {
        clearContentSpace()
        clearDataSpace()
        setDeleteFeedback({ target: valueToDelete, msg: data })
        setTimeout(() => setDeleteFeedback(null), 3000)
      },
    })
  }

  // ---- account settings ----
  function changeAccount(action, typedValue, retypedValue, setBtn) {
    const flash = (color, label) => {
      setBtn({ color, label })
      setTimeout(() => setBtn({ color: null, label: 'Change' }), 3000)
    }

    if (typedValue !== retypedValue) return flash('red', "Values don't match. Please reinsert")
    if (typedValue === '' || retypedValue === '') return flash('red', 'One or more field are empty. Please retry')

    $.ajax({
      url: 'server.php',
      dataType: 'json',
      cache: false,
      data: { usr: paramsRef.current.usr, typedValue, action },
      type: 'post',
      success: (data) => {
        if (action === 'change-mail') setUsr(data['user_mail'])
        flash('green', data['value'])
      },
    })
  }

  // ---- search ----
  function searchData() {
    const s = paramsRef.current

    if (s.usr === '') {
      setSearchBtn({ color: 'red', label: 'You must login before' })
      setTimeout(() => setSearchBtn({ color: null, label: 'Search' }), 3000)
      return
    }

    let dtsSn = ''
    if (sna.dataToSearch !== '') dtsSn = JSON.parse(sna.dataToSearch)['sn']

    if (s.sn === dtsSn) setEnvironment()
    else setSliders(s.usr, s.sn)
  }

  // ---- data panel tabs ----
  function tipOrSpinner(viz1, viz2) {
    if (viz1 === 'selected') {
      const what = viz2 === 'links' ? 'link' : 'node'
      $('.data').append('<div class="data-item"><span> Try to select a ' + what + ' </span></div>')
    } else {
      showDataSpinner()
    }
  }

  function handleDataViz1(v) {
    setDataViz1(v)
    sna.dataViz1 = v
    clearDataSpace()

    if (!sna.dataToSearch) return

    const dts = JSON.parse(sna.dataToSearch)
    dts['dataViz1'] = v
    sna.dataToSearch = JSON.stringify(dts)

    const s = paramsRef.current
    const ntd = getNodeToDisplay(dts['graphType'], dts['sn'], s)

    $.ajax({
      url: 'server.php',
      dataType: 'json',
      data: { dataToSearch: sna.dataToSearch, action: 'getData', ntd },
      type: 'post',
      beforeSend: () => tipOrSpinner(v, dts['dataViz2']),
      success: (data) => dataVisualization(data),
      error: () => console.log('errore'),
    })
  }

  function handleDataViz2(v) {
    setDataViz2(v)
    sna.dataViz2 = v
    setSortValue(v === 'links' ? 'tagcount' : 'timedesc')
    clearDataSpace()

    if (!sna.dataToSearch) return

    const dts = JSON.parse(sna.dataToSearch)
    dts['dataViz2'] = v
    sna.dataToSearch = JSON.stringify(dts)

    const s = paramsRef.current
    const ntd = getNodeToDisplay(dts['graphType'], dts['sn'], s)

    $.ajax({
      url: 'server.php',
      dataType: 'json',
      data: { dataToSearch: sna.dataToSearch, action: 'getData', ntd },
      type: 'post',
      beforeSend: () => tipOrSpinner(dts['dataViz1'], v),
      success: (data) => dataVisualization(data),
      error: () => console.log('errore2'),
    })
  }

  function handleSort(v) {
    setSortValue(v)

    if (!sna.dataToSearch) return

    const s = paramsRef.current
    const rangeValue = s.dataViz1

    const dts = JSON.parse(sna.dataToSearch)
    dts['sortValue'] = v
    sna.dataToSearch = JSON.stringify(dts)

    const ntd = getNodeToDisplay(dts['graphType'], dts['sn'], s)

    if (rangeValue === 'filtered' || rangeValue === 'all')
      $.ajax({
        url: 'server.php',
        dataType: 'json',
        cache: false,
        data: { dataToSearch: sna.dataToSearch, action: 'getData', ntd },
        type: 'post',
        beforeSend: showDataSpinner,
        success: (data) => dataVisualization(data),
        error: () => {
          if (s.usr !== '')
            $('.data').html('<div class="row"><div class="col-12">Select an element in the graph</div></div>')
          else clearDataSpace()
        },
      })
  }

  // ---- render ----
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <Group component="nav" px="md" py={8} gap="sm" style={{ flexShrink: 0 }} bg="var(--mantine-color-dark-6)">
        <Burger opened={drawerOpened} onClick={drawer.toggle} aria-label="Toggle drawer"
          color="var(--mantine-primary-color-filled)" />
        <Title order={3} style={{ cursor: 'default', color: 'var(--mantine-primary-color-filled)' }}>
          Social Network Analysis
        </Title>
      </Group>

      <SideDrawer
        opened={drawerOpened}
        onClose={drawer.close}
        usr={usr}
        onLogin={login}
        onRegister={register}
        onLogout={logout}
        onOpenHelp={() => { drawer.close(); help.open() }}
        onUpload={uploadDump}
        upload={upload}
        onDeleteDump={deleteDump}
        deleteFeedback={deleteFeedback}
        onChangeMail={(a, b) => changeAccount('change-mail', a, b, setChangeMailBtn)}
        onChangePassword={(a, b) => changeAccount('change-password', a, b, setChangePassBtn)}
        changeMailBtn={changeMailBtn}
        changePassBtn={changePassBtn}
        loginFeedback={loginFeedback}
        registerBtn={registerBtn}
      />

      <HelpModal opened={helpOpened} onClose={help.close} />

      <div style={{ flex: 1, minHeight: 0, display: 'flex', flexDirection: 'column', padding: '12px 16px 16px' }}>
        <FiltersMenu
          sn={sn} onSnChange={setSn}
          keyword={keyword} onKeywordChange={setKeyword}
          person={person} onPersonChange={setPerson}
          nodeVal={nodeVal} nodeMax={nodeMax}
          onNodeChange={setNodeVal}
          onNodeChangeEnd={(v) => setEnvironment({ nodeVal: v })}
          edgeVal={edgeVal} edgeMax={edgeMax}
          onEdgeChange={setEdgeVal}
          onEdgeChangeEnd={(v) => setEnvironment({ edgeVal: v })}
          dateBounds={dateBounds} dateRange={dateRange}
          onDateChange={setDateRange}
          onDateChangeEnd={(v) => setEnvironment({ dateRange: v })}
          onSearch={searchData}
          searchBtn={searchBtn}
        />

        <MainSection
          active={usr !== ''}
          sn={sn}
          graphType={graphType}
          onGraphTypeChange={(v) => { setGraphType(v); setEnvironment({ graphType: v }) }}
          fbUserType={fbUserType} onFbUserType={(v) => { setFbUserType(v); setEnvironment({ fbUserType: v }) }}
          fbNodeType={fbNodeType} onFbNodeType={(v) => { setFbNodeType(v); setEnvironment({ fbNodeType: v }) }}
          fbMap={fbMap} onFbMap={(v) => { setFbMap(v); setEnvironment({ fbMap: v }) }}
          twUserType={twUserType} onTwUserType={(v) => { setTwUserType(v); setEnvironment({ twUserType: v }) }}
          tweetType={tweetType} onTweetType={(v) => { setTweetType(v); setEnvironment({ tweetType: v }) }}
          twNodeType={twNodeType} onTwNodeType={(v) => { setTwNodeType(v); setEnvironment({ twNodeType: v }) }}
          onStabilize={stabilizeGraph}
          dataViz1={dataViz1} onDataViz1={handleDataViz1}
          dataViz2={dataViz2} onDataViz2={handleDataViz2}
          sortValue={sortValue} onSortChange={handleSort}
        />
      </div>
    </div>
  )
}