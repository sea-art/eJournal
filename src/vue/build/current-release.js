const fs = require('fs')

const packageJSON = fs.readFileSync('./package.json')
const version = JSON.parse(packageJSON).version || 0

const currentRelease = {
    version,
}

module.exports = currentRelease
