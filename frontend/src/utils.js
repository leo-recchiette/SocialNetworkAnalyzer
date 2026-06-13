// Pure helpers ported from the old static/main.js

export function getTodayDate(when) {
  let d = new Date()

  let month = d.getMonth() + 1
  let day = d.getDate()

  let today
  if (when === 'today')
    today = d.getFullYear() + '.' +
      (('' + month).length < 2 ? '0' : '') + month + '.' +
      (('' + day).length < 2 ? '0' : '') + day
  else
    today = (d.getFullYear() - 1) + '.' +
      (('' + month).length < 2 ? '0' : '') + month + '.' +
      (('' + day).length < 2 ? '0' : '') + day

  return today.toString()
}

export function formatDate(date) {
  var d = new Date(date),
    month = '' + (d.getMonth() + 1),
    day = '' + d.getDate(),
    year = d.getFullYear()

  if (month.length < 2) month = '0' + month
  if (day.length < 2) day = '0' + day

  return [year, month, day].join('/')
}

export function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return re.test(email)
}

export function dataToSearchJSONCreator(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr, graphType, dataViz1, dataViz2, sortValue) {
  let obj = new Object()
  obj.keyword = keyword
  obj.person = person
  obj.start_date = start_date
  obj.end_date = end_date
  obj.minNodevalue = minNodevalue
  obj.minEdgeValue = minEdgeValue
  obj.sn = sn
  obj.graphType = graphType
  obj.dataViz1 = dataViz1
  obj.dataViz2 = dataViz2
  obj.usr = usr
  obj.sortValue = sortValue

  return JSON.stringify(obj)
}

export function epochToDateLabel(sec) {
  return formatDate(new Date(sec * 1000).toDateString())
}