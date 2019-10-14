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
    setFilteredJournals (journals, order = true, groupName = null, searchValue = null, sortBy = 'name') {
        if (this.debug) { console.log('setFilteredJournals triggered with', journals) }
        function compare (a, b) {
            if (a < b) { return order ? 1 : -1 }
            if (a > b) { return order ? -1 : 1 }
            return 0
        }

        const sortOptions = {
            name: (a, b) => compare(a.student.full_name, b.student.full_name),
            username: (a, b) => compare(a.student.username, b.student.username),
            markingNeeded: (a, b) => compare(a.stats.submitted - a.stats.graded, b.stats.submitted - b.stats.graded),
            points: (a, b) => compare(a.stats.acquired_points, b.stats.acquired_points),
        }

        function groupFilter (journal) {
            const groups = []
            journal.students.forEach((student) => {
                if (student.user.groups) {
                    student.user.groups.forEach((group) => {
                        if (!groups.includes(group)) {
                            groups.push(group.name)
                        }
                    })
                }
            })
            if (groups === []) {
                return false
            }
            return groups.map(g => g.name).includes(groupName)
        }

        function searchFilter (journal) {
            return journal.names.toLowerCase().includes(searchValue.toLowerCase())
                || journal.full_names.toLowerCase().includes(searchValue.toLowerCase())
        }
        let filteredJournals = journals
        if (groupName !== null) {
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
