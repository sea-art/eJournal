/* Expects a start date of the format "YY-mm-dd" */
export default {
    yearOffset (startDate) {
        const split = startDate.split('-')

        if ((split[1] === '2' || split[1] === '02') && split[2] === '29') {
            split[2] = '01'
            split[1] = '03'
        }

        const yearOff = parseInt(split[0], 10) + 1

        split[0] = String(yearOff)
        return split.join('-')
    },

    /* Converts an arraybuffer response to a humanreadable text. */
    parseArrayBuffer (arrayBuffer) {
        const enc = new TextDecoder('utf-8')

        return JSON.parse(enc.decode(arrayBuffer))
    },
}
