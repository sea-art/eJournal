<script>
export default {
    debug: false,
    state: {
        breadCrumb: [],
        format: { templatePool: [], nodes: [] }
    },
    setBreadcrumb (breadCrumbInternalList) {
        if (this.debug) { console.log('setBreadcrumb triggered with', breadCrumbInternalList) }
        this.state.breadCrumb = breadCrumbInternalList.slice() // safety slice
    },
    setFormat (templatePool, nodes) {
        if (this.debug) { console.log('setFormat triggered with', templatePool, nodes) }
        this.state.format.templatePool = templatePool
        this.state.format.nodes = nodes
    },
    clearFormat () {
        this.state.format = { templatePool: [], nodes: [] }
    },
    debugOn () {
        this.debug = true
    },
    debugOff () {
        this.debug = false
    }
}
</script>
