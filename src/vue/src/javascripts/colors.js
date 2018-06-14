function getColors(item_count) {
    var colors = ['pink-border', 'peach-border', 'blue-border']
    var retval = []
    var quotient = Math.floor(item_count / colors.length)
    var remainder = item_count % colors.length

    for (var i = 0; i < quotient; i++) {
        retval = retval.concat(colors);
    }

    return retval.concat(colors.slice(0, remainder))
}

export default getColors
