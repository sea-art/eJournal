<script>
export default {
    debug: false,
    state: {
        cachedMap: {},
        format: { templatePool: [], nodes: [] },
        filteredJournals: [],
    },
    setCachedMap (cachedMap) {
        if (this.debug) { console.log('setCachedMap triggered with', cachedMap) }
        this.state.cachedMap = cachedMap
    },
    setFormat (templatePool, nodes) {
        if (this.debug) { console.log('setFormat triggered with', templatePool, nodes) }
        this.state.format.templatePool = templatePool
        this.state.format.nodes = nodes
    },
    setFilteredJournals (journals, order = true, groups = null, searchValue = null, sortBy = 'name') {
        if (this.debug) { console.log('setFilteredJournals triggered with', journals) }
        function compare (a, b) {
            if (a < b) { return order ? 1 : -1 }
            if (a > b) { return order ? -1 : 1 }
            return 0
        }

        const sortOptions = {
            name: (a, b) => compare(a.name, b.name),
            username: (a, b) => {
                if (a.authors.length > 0 && b.authors.length > 0) {
                    return compare(a.authors[0].user.username, b.authors[0].user.username)
                } else if (a.authors.length > 0) {
                    return -1
                } else if (b.authors.length > 0) {
                    return 1
                }
                return 0
            },
            markingNeeded: (a, b) => compare(a.stats.submitted - a.stats.graded, b.stats.submitted - b.stats.graded),
            points: (a, b) => compare(a.stats.acquired_points, b.stats.acquired_points),
        }

        function groupFilter (journal) {
            const groupsList = []
            journal.authors.forEach((student) => {
                if (student.user.groups) {
                    student.user.groups.forEach((group) => {
                        if (!groupsList.includes(group)) {
                            groupsList.push(group)
                        }
                    })
                }
            })
            if (groups === null) {
                return false
            }
            return groups.some(group => groupsList.includes(group))
        }

        function searchFilter (journal) {
            return journal.name.toLowerCase().includes(searchValue.toLowerCase())
                || journal.authors.some(user => user.user.username.toLowerCase().includes(searchValue.toLowerCase()))
                || journal.authors.some(user => user.user.full_name.toLowerCase().includes(searchValue.toLowerCase()))
        }
        let filteredJournals = journals
        if (groups !== null && groups.length !== 0) {
            filteredJournals = filteredJournals.filter(groupFilter)
        }
        if (searchValue !== null && searchValue !== '') {
            filteredJournals = filteredJournals.filter(searchFilter)
        }
        filteredJournals.sort(sortOptions[sortBy])
        this.state.filteredJournals = filteredJournals
    },
    clearFormat () {
        this.state.format = { templatePool: [], nodes: [] }
    },
    debugOn () {
        this.debug = true
    },
    debugOff () {
        this.debug = false
    },
    clearCache () {
        this.state.cachedMap = []
    },
}
</script>
