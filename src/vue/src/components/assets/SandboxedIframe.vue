<template>
    <iframe
        sandbox="allow-same-origin allow-popups"
        frameBorder="0"
        marginwidth="0"
        marginheight="0"
        scrolling="no"
        class="w-100 theme-iframe"
        @load="loadedIframe"
    />
</template>

<script>
export default {
    name: 'SandboxedIframe',
    props: {
        content: {
            type: String,
            required: true,
        },
    },
    data () {
        return {
            iframe: null,
        }
    },
    watch: {
        content () {
            this.setContent()
        },
    },
    methods: {
        loadedIframe (e) {
            this.iframe = e.target
            window.addEventListener('resize', this.fitContent)
            this.setCustomStyle()
            this.setLinkTarget()
            this.setContent()
        },
        setContent () {
            if (this.iframe && this.iframe.contentWindow) {
                this.iframe.contentWindow.document.body.innerHTML = this.content
                this.fitContent()
            }
        },
        fitContent () {
            if (this.iframe && this.iframe.contentWindow) {
                this.iframe.height = 0
                this.iframe.height = this.iframe.contentWindow.document.body.scrollHeight
            }
        },
        setCustomStyle () {
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
            const style = document.createElement('style')
            style.type = 'text/css'
            style.appendChild(document.createTextNode(css))
            this.iframe.contentWindow.document.head.append(style)
        },
        setLinkTarget () {
            const base = document.createElement('base')
            base.target = '_blank'
            this.iframe.contentWindow.document.head.append(base)
        },
    },
}
</script>
