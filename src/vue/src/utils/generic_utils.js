export default {
    /* Converts an arraybuffer response to a humanreadable text. */
    parseArrayBuffer (arrayBuffer) {
        const enc = new TextDecoder('utf-8')

        return JSON.parse(enc.decode(arrayBuffer))
    },

    invalidAccessToken (error) {
        if (error) {
            let code
            if (error.response.data instanceof ArrayBuffer) {
                code = this.parseArrayBuffer(error.response.data).code
            } else {
                code = error.response.data.code
            }

            return code === 'token_not_valid'
        } else {
            return false
        }
    },
}
