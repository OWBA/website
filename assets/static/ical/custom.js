function UTC_to_DE(date) {
  if (date.slice(-1) != 'Z') { return date; }
  let d = new Date(date);
  let a = new Date(d.getFullYear(), 3, 0, 3);
  let b = new Date(d.getFullYear(), 10, 0, 4);
  a.setDate(a.getDate() - a.getDay());
  b.setDate(b.getDate() - b.getDay());
  return date.slice(0,-1) + ((a < d && d < b) ? '-0200' : '-0100');
}
function transform_event(event) {
  if ('start' in event) { event['start'] = UTC_to_DE(event['start']); }
  if ('end' in event) { event['end'] = UTC_to_DE(event['end']); }
  event['url'] = '#';  // set cursor pointer for event popup
  return event;
}
function calendar_load_json(url, params={}) {
  var done = false;
  params['events'] = (info, success, failure) => {
    if (done) { return; }
    done = true;
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 400) {
        success(JSON.parse(xhr.responseText), xhr);
      } else {
        failure('Request failed', xhr);
      }
    }
    xhr.onerror = () => failure('Request failed', xhr);
    xhr.send(null);
  };
  return params;
}
function hasClass(element, className) {
  return (' ' + element.className + ' ').indexOf(' ' + className+ ' ') > -1;
}
function event_color(evElem) {
  if (hasClass(evElem, 'fc-daygrid-dot-event')) {
    return evElem.querySelector('.fc-daygrid-event-dot').style.borderColor;
  } else if (hasClass(evElem, 'fc-list-event')) {
    return evElem.querySelector('.fc-list-event-dot').style.borderColor;
  } else {  // fc-daygrid-event, fc-timegrid-event
    return evElem.style.borderColor
  }
}
function format_event_date(event) {
  var fmt = {
    month: 'long',
    year: 'numeric',
    day: 'numeric',
    weekday: 'short',
  };
  if (event.allDay) {
    end = event.end - 1;  // else will print next day
  } else {
    end = event.end;
    fmt.hour = '2-digit';
    fmt.minute = '2-digit';
    fmt.omitZeroMinute = true;
  }
  return event._context.calendarApi.formatRange(event.start, end, fmt);
}
function plain_anchor(link) {
  if (!link) { return link; }
  let a = document.createElement('A');
  a.href = link;
  a.appendChild(document.createTextNode(link));
  return a;
}
let re_http_email = /https?:\/\/[^\s]+[^\s.,;]|[^\s]+@owba\.de/g;
function detect_url_and_email(text) {
  if (!text) { return text; }
  text = text.replace(/\n/g, '<br>');
  var idx = 0;
  var tmp = document.createElement('SPAN');
  var match;
  while (match = re_http_email.exec(text)) {
    tmp.innerHTML += text.substring(idx, match.index);
    let a = tmp.appendChild(plain_anchor(match[0]));
    if (match[0].slice(-8) === '@owba.de') {
      a.href = 'mailto:' + match[0];
    }
    idx = match.index + match[0].length;
  }
  tmp.innerHTML += text.substring(idx);
  return tmp;
}
function make_itemized_body(entries) {
  let body = document.createElement('DIV');
  for (var i = 0; i < entries.length; i++) {
    var detail = entries[i][0];
    if (!detail) { continue; }
    if (typeof detail === 'string') {
      detail = document.createTextNode(detail);
    }
    if (entries[i].length == 2) {
      let icon = body.appendChild(document.createElement('DIV'));
      icon.className = 'icon-entry';
      icon.innerHTML = entries[i][1];
      icon.appendChild(detail);
    } else {
      body.appendChild(document.createElement('P')).appendChild(detail);
    }
  }
  return body;
}
function click_on_event(info) {
  info.jsEvent.preventDefault();  // prevent open url
  let color = event_color(info.el) || '#3788D8';
  function svg_icon(name) {
    return '<svg style="fill: ' + color + '"><use href="/static/icons.svg#' + name + '"/></svg>';
  }
  var body = [
    [detect_url_and_email(info.event.extendedProps.desc)],
    [format_event_date(info.event), svg_icon('time')],
    [detect_url_and_email(info.event.extendedProps.place), svg_icon('place')],
    [plain_anchor(info.event.extendedProps.link), svg_icon('link')],
  ];
  show_modal(info.event.title, make_itemized_body(body), color);
}
function init_calendar(cal_id, options) {
  document.addEventListener('DOMContentLoaded', function() {
    options.timeZone = 'UTC';  // required for transform_event
    options.eventDataTransform = transform_event; // UTC -> DE
    options.eventClick = click_on_event;
    // remove let to allow manipulation
    let calendar = new FullCalendar.Calendar(document.getElementById(cal_id), options);
    calendar.render();
  });
}

// Open Modal Popup Window
function show_modal(title, body, color='#CC287A') {
  // outer click area
  let modal = document.body.appendChild(document.createElement('DIV'));
  modal.className = 'app-modal';
  function close_modal() {
    modal.remove();
    window.onmousedown = null;
    window.onkeydown = null;
  }
  window.onmousedown = function(e) { if (e.target == modal) close_modal(); };
  window.onkeydown = function(e) { if (e.key == "Escape") close_modal(); };
  // inner box
  let box = modal.appendChild(document.createElement('DIV'));
  box.className = 'modal-box';
  box.style.borderColor = color;
  // close button
  let close = box.appendChild(document.createElement('SPAN'));
  close.className = 'modal-close';
  close.innerHTML = '&times;';
  close.onclick = close_modal;
  // box title
  let header = box.appendChild(document.createElement('H4'));
  header.className = 'modal-title';
  header.style.background = color;
  // actual content
  let content = box.appendChild(document.createElement('P'));
  content.className = 'modal-content';
  // set user-content
  header.innerHTML = title || '';
  if (typeof body === 'string') {
    content.innerHTML = body;
  } else {
    content.appendChild(body);
  }
}
