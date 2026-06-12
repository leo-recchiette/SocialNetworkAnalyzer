import $ from 'jquery'

// Helpers around the two imperative containers (.content and .data) that the
// legacy visualization modules render into. React renders those divs once and
// never touches their children.

export function clearDataSpace() {
  $('.data').html('')
}

export function clearContentSpace() {
  $('.content').html('')
}

export function showDataSpinner() {
  $('.data').html(
    '<div class="row">' +
    '<div class="col-4"></div>' +
    '<div class="col-4">' +
    '<div class="loading-spinner" role="status" style="margin-top:5px; margin-left: 42%"></div>' +
    '</div>' +
    '<div class="col-4"></div>' +
    '</div>')
}

export function noDataFoundVisualization() {
  $('.data').html(
    '<div class="noDataFound"><i class=" text-center material-icons">error</i></div>' +
    '<div class="noDataFound">There isn’t any data that can satisfy your research</div>'
  )
}