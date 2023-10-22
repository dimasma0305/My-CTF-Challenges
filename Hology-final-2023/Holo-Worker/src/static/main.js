const w = new Worker("./worker.mjs", { "type": "module" })
function add(title, description) {
  w.postMessage({ case: "add", title, description })
}
if (location.hash === "#test") {
  w.postMessage({ case: "add", title: "test", description: "test" })
}
w.onmessage = (ev) => {
  let html = ""
  ev.data.forEach((v) => {
    html += `
    <tr id="data" class="table-primary">
      <td>${v.title}<\/td>
      <td>${v.description}<\/td>
    <\/tr>`
  })
  document.getElementById("data").setHTML(html)
}
setTimeout(() => {
  const url = new URL(location)
  const params = url.searchParams
  if (params.has("filter")) {
    filter(params.get("filter"))
  } else {
    w.postMessage({ case: "getAll" })
  }
}, 1000)

function addNote(title, description) {
  w.postMessage({ case: "add", title, description })
}
function deleteAll() {
  w.postMessage({ case: "deleteAll" })
}
function filter(filter) {
  if (filter == "") return
  w.postMessage({ case: "filterNotes", filter })
}
