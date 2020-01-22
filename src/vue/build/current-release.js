const execFileSync = require('child_process').execFileSync
const version = execFileSync('git', ['for-each-ref', '--format="%(refname:short)"', '--sort=-authordate', '--count=1', 'refs/tags']).toString().trim()
const rawMessage = execFileSync('git', ['tag', '-l', '-n3', version]).toString().split(/\n\s*\n/)
const date = new Date(execFileSync('git', ['tag', '-l', '-n1', '--format=\'%(taggerdate)\'', version]).toString()
    .trim())

const currentRelease = {
    version,
    message: rawMessage.length > 1 ? rawMessage[1] : '',
    date,
}

module.exports = currentRelease
