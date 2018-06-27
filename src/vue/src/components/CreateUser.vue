<template>
    <div>
        <b-form @submit="onSubmit" @reset="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.username" placeholder="Username" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.password" placeholder="Password" required/>
            <b-button class="float-right" type="reset">Reset</b-button>
            <b-button class="float-right" type="submit">Create</b-button>
        </b-form>
    </div>
</template>

<script>
export default {
    name: 'CreateUser',
    props: ['lti'],
    data () {
        return {
            form: {
                username: '',
                password: '',
            }
        }
    },
    methods: {
        onSubmit () {
            // TODO: Call right api to create user and emit UID to parent.
            //
            // courseApi.create_new_course(this.form.courseName,
            //     this.form.courseAbbr, this.form.courseStartdate,
            //     this.form.ltiCourseID)
            //     .then(response => {
            //         this.$emit('handleAction', response.course.cID)
            //         this.onReset(undefined)
            //     })
        },
        onReset (evt) {
            if (evt !== undefined) {
                evt.preventDefault()
            }

            /* Reset our form values */
            this.form.username = ''
            this.form.password = ''

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    },
}
</script>
