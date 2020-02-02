const execFileSync = require('child_process').execFileSync
const version = ""
const rawMessage = ""
const date = ""

const currentRelease = {
    version,
    message: rawMessage.length > 1 ? rawMessage[1] : '',
    date,
}

module.exports = currentRelease
