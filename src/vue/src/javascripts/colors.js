function getColors (itemCount) {
    var colors = ['pink-border', 'peach-border', 'blue-border']
    var retval = []
    var quotient = Math.floor(itemCount / colors.length)
    var remainder = itemCount % colors.length

    for (var i = 0; i < quotient; i++) {
        retval = retval.concat(colors)
    }

    return retval.concat(colors.slice(0, remainder))
}

export default getColors
