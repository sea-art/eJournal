import axios from 'axios'

function setImgSrc (el, binding) {
    /* Only get the img on initilisation or when the url is changed */
    if (binding.oldValue === undefined || binding.value !== binding.oldValue) {
        const imageUrl = binding.value

        axios({ method: 'get', url: imageUrl, responseType: 'arraybuffer' })
            .then((resp) => {
                const mimeType = resp.headers['content-type'].toLowerCase()
                const imgBase64 = Buffer.from(resp.data, 'binary').toString('base64')
                el.src = `data:${mimeType};base64,${imgBase64}`
            /* If the conversion fails, fallback to the default url */
            })
            .catch(() => {
                el.src = imageUrl
            })
    }
}

export default {
    install (Vue) {
        Vue.directive('auth-image', {
            bind: (el, binding) => { setImgSrc(el, binding) },
            componentUpdated: (el, binding) => { setImgSrc(el, binding) },
        })
    },
}
