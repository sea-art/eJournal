import VueSanitize from 'vue-sanitize'

const OPTIONS_CONFIG = {
    allowedTags: [
        'h3', 'h4', 'h5', 'h6', 'blockquote', 'p', 'a', 'ul', 'ol',
        'nl', 'li', 'b', 'i', 'strong', 'em', 'strike', 'code', 'hr', 'br', 'div',
        'table', 'thead', 'caption', 'tbody', 'tr', 'th', 'td', 'pre', 'iframe'
    ],
    allowedAttributes: {
        a: [ 'href', 'name', 'target' ],
        // We don't currently allow img itself by default, but this
        // would make sense if we did
        img: [ 'src' ]
    },
    // Lots of these won't come up by default because we don't allow them
    selfClosing: [ 'img', 'br', 'hr', 'area', 'base', 'basefont', 'input', 'link', 'meta' ],
    // URL schemes we permit
    allowedSchemes: [ 'http', 'https', 'ftp', 'mailto' ],
    allowedSchemesByTag: {},
    allowedSchemesAppliedToAttributes: [ 'href', 'src', 'cite' ],
    allowProtocolRelative: true,
    allowedIframeHostnames: ['www.youtube.com', 'player.vimeo.com']
}

export default function setup (vue) {
    vue.use(VueSanitize, OPTIONS_CONFIG)
}
