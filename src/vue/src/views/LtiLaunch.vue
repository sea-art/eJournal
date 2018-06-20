<template>
    <div>
        <h1>Lti Lauch page komt error want anders redirect</h1>
        {{msg}}
        {{jwt_refresh}}
    </div>
</template>

<script>
export default {
    name: 'LtiLaunch',
    data () {
        return {
            msg: 'unsuccesfull',
            jwt_refresh: ':('
        }
    },
    created () {
        localStorage.setItem('jwt_access', this.$route.query.jwt_access)
        localStorage.setItem('jwt_refresh', this.$route.query.jwt_refresh)
        this.msg = this.$route.query.jwt_access
        this.jwt_refresh = this.$route.query.jwt_refresh
        /* Get the IDs of the objects out of the query. */
        var jID = this.$route.query.jID
        var aID = this.$route.query.aID
        var cID = this.$route.query.cID
        var student = this.$route.query.student

        if (student) {
            /* If a student requests this. */
            if (cID === 'undefined' || aID === 'undefined') {
                // TODO Push a 404.
            } else if (jID === 'undefined') {
                this.$router.push({name: 'Assignment', params: {cID: cID, aID: aID}})
            } else {
                this.$router.push({name: 'Journal', params: {cID: cID, aID: aID, jID: jID}})
            }
        } else {
            /* If a non student requests this. */
            if (cID === 'undefined') {
                // TODO creation
            } else if (aID === 'undefined') {
                // TODO creation
            } else {
                this.$router.push({name: 'Assignment', params: {cID: cID, aID: aID}})
            }
        }
    }
}
</script>
