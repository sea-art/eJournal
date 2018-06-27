<template>
    <div>
        <b-form @submit="onSubmit" @reset="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.username" placeholder="Username" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.password" placeholder="Password" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"  v-model="form.email" placeholder="Email" required/>
            <b-button class="float-right" type="reset">Reset</b-button>
            <b-button class="float-right" type="submit">Create</b-button>
        </b-form>
    </div>
</template>

<script>
export default {
    name: 'RegisterUser',
    props: ['lti'],
    data () {
        return {
            form: {
                username: '',
                password: '',
                firstname: '',
                lastname: '',
                email: '',
                ltiJWT: ''
            }
        }
    },
    methods: {
        onSubmit () {
            userApi.createUser(this.form.username, this.form.password,
                               this.form.firstname, this.form.lastname,
                               this.form.email, this.form.ltiJWT)
        },
        onReset (evt) {
            if (evt !== undefined) {
                evt.preventDefault()
            }

            /* Reset our form values */
            this.form.username = ''
            this.form.password = ''
            this.form.firstname = ''
            this.form.lastname = ''
            this.form.email = ''

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    }
}
</script>
