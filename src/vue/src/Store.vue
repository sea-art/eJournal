<script>
export default {
    debug: false,
    state: {
        breadCrumb: []
    },
    setBreadcrumb (breadCrumbInternalList) {
        if (this.debug) { console.log('setBreadcrumb triggered with', breadCrumbInternalList) }
        this.state.breadCrumb = breadCrumbInternalList.slice() // safety slice
    },
    debugOn () {
        this.debug = true
    },
    debugOff () {
        this.debug = false
    }
}
</script>
