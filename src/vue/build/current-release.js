const execFileSync = require('child_process').execFileSync

const version = execFileSync('git', ['describe', '--abbrev=0', '--tags']).toString().trim()
const rawMessage = execFileSync('git', ['tag', '-l', '-n3', version]).toString().split(/\n\s*\n/)
const date = new Date(execFileSync('git', ['tag', '-l', '-n1', '--format=\'%(taggerdate)\'', version]).toString().trim())

const currentRelease = {
    version,
    message: rawMessage.length > 1 ? rawMessage[1] : '',
    date
}

module.exports = currentRelease
