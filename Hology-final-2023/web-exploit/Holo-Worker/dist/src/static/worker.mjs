const request = indexedDB.open("database")
let store;

request.addEventListener("error", (ev) => {
    console.error(ev.target.error)
})

const asyncFilter = async (arr, predicate) => {
    const results = await Promise.all(arr.map(predicate));
    return arr.filter((_v, index) => results[index]);
}

class Note {
    getStore() {
        return request.result.transaction("notes", "readwrite").objectStore("notes")
    }
    getNotes() {
        return new Promise((resolve, reject) => {
            const request = this.getStore().getAll()
            request.onsuccess = () => resolve(request.result)
            request.onerror = (e) => reject(e)
        })
    }
    getNotesKeys() {
        return new Promise((resolve, reject) => {
            const request = this.getStore().getAllKeys()
            request.onerror = (e) => reject(e)
            request.onsuccess = () => resolve(request.result)
        })
    }
    addNote(title, description) {
        this.getStore().add({ title, description })
    }
    deleteNotes() {
        return new Promise((resolve, reject) => {
            this.getNotesKeys().then(keys => {
                keys.forEach((v) => {
                    this.getStore().delete(v)
                })
                resolve()
            })
        })
    }
    getNotesBy(filter) {
        return new Promise((resolve) => {
            this.getNotes().then(async notes => {
                const filteredNotes = await asyncFilter(notes, filter)
                resolve(filteredNotes)
            })
        })
    }
}

request.addEventListener("upgradeneeded", () => {
    store = request.result.createObjectStore("notes", { keyPath: "id", autoIncrement: true })
    store.createIndex("title", "title", { "unique": true })
    store.createIndex("description", "description")
})

request.addEventListener("success", () => {
    const note = new Note()
    self.addEventListener("message", async (ev) => {
        switch (ev.data.case) {
            case "add":
                note.addNote(ev.data.title, ev.data.description)
                self.postMessage(await note.getNotes(), { targetOrigin: ev.origin })
                break;
            case "getAll":
                self.postMessage(await note.getNotes(), { targetOrigin: ev.origin })
                break;
            case "deleteAll":
                await note.deleteNotes()
                self.postMessage(await note.getNotes(), { targetOrigin: ev.origin })
                break;
            case "filterNotes":
                const usrFunc = Function("note", ev.data.filter)
                self.postMessage(await note.getNotesBy(usrFunc), { targetOrigin: ev.origin })
            default:
                break;
        }
    })
})

