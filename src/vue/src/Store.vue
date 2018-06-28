<script>
export default {
    debug: false,
    state: {
        cachedMap: [],
        format: { templatePool: [], nodes: [] },
        filteredJournals: []
    },
    setCachedMap (cachedMap) {
        if (this.debug) { console.log('setCachedMap triggered with', cachedMap) }
        this.state.cachedMap = cachedMap.slice()
    },
    setFormat (templatePool, nodes) {
        if (this.debug) { console.log('setFormat triggered with', templatePool, nodes) }
        this.state.format.templatePool = templatePool
        this.state.format.nodes = nodes
    },
    setFilteredJournals (filteredJournals) {
        if (this.debug) { console.log('setFilteredJournals triggered with', filteredJournals) }
        this.state.filteredJournals = filteredJournals.slice()
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
