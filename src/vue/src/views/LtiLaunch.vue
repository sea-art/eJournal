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
        var student = this.$route.query.student
        var assign = this.$route.query.assign
        var course = this.$route.query.course
        if (student === "undefined") {
            this.$router.push({name:"Assignment", params: {course:course, assign:assign}})
        } else {
            this.$router.push({name:"Journal", params: {course:course, assign:assign, student:student}})
        }
    }
}
</script>
