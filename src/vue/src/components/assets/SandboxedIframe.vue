<template>
    <iframe
        @load="init($event)"
        sandbox="allow-same-origin allow-popups"
        frameBorder="0"
        marginwidth="0"
        marginheight="0"
        scrolling="no"
        class="w-100 theme-iframe"
    />
</template>

<script>
export default {
    name: 'SandboxedIframe',
    props: {
        content: {
            type: String,
            required: true
        }
    },
    data () {
        return {
            iframe: null
        }
    },
    computed: {
        // QUESTION: How does one watch this.$root.windowWidth directly?
        windowWidth: function () {
            return this.$root.windowWidth
        }
    },
    watch: {
        windowWidth () {
            if (this.iframe) { this.scaleIframe(this.iframe) }
        }
    },
    methods: {
        scaleIframe (obj) {
            obj.height = 0
            obj.height = obj.contentWindow.document.body.offsetHeight + 'px'
        },
        injectContent (obj) {
            let doc = obj.contentWindow.document
            doc.open()
            doc.write(this.content)
            doc.close()
        },
        setCustomStyle (obj) {
            let doc = obj.contentWindow.document
            const css = `
body {
    font-family: 'Roboto', sans-serif;
    color: #252C39;
}

p a {
    text-decoration: none;
    color: #22648A;
}

img {
    max-width: 100%;
    height: auto
}`

            let style = document.createElement('style')
            style.type = 'text/css'
            style.appendChild(document.createTextNode(css))
            doc.head.append(style)
        },
        setLinkTarget (obj) {
            let doc = obj.contentWindow.document
            let base = document.createElement('base')
            base.target = '_blank'
            doc.head.append(base)
        },
        init (e) {
            this.injectContent(e.target)
            this.setCustomStyle(e.target)
            this.setLinkTarget(e.target)
            this.scaleIframe(e.target)
            this.iframe = e.target
        }
    }
}
</script>
