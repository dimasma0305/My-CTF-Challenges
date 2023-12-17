let id = location.pathname.split("/").pop()
fetch("/api/v1/note/"+id).then(async res =>{
    document.getElementById("content").innerHTML = await res.text()
})