<template>
    <div>
        <b-card class="blue-border no-hover card-last-elem-button">
            <b-form @submit.prevent="onSubmit" @reset.prevent="onReset">
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.username" placeholder="Username" required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"  v-model="form.firstname" placeholder="Firstname" required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"  v-model="form.lastname" placeholder="Lastname" required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.password" type="password" placeholder="Password" required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.password2" type="password" placeholder="Password (again)" required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"  v-model="form.email" placeholder="Email" required/>
                <b-button class="float-left delete-button multi-form" type="reset">Reset</b-button>
                <b-button class="float-right add-button multi-form" type="submit">Register</b-button>
            </b-form>
        </b-card>
    </div>
</template>

<script>
import auth from '@/api/auth.js'
import userApi from '@/api/user.js'

export default {
    name: 'RegisterUser',
    props: ['lti'],
    data () {
        return {
            form: {
                username: '',
                password: '',
                password2: '',
                firstname: '',
                lastname: '',
                email: '',
                ltiJWT: ''
            }
        }
    },
    methods: {
        checkInput () {
            var correctInput = true

            if (this.form.password !== this.form.password2) {
                this.$toasted.error('The given passwords do not match!')
                correctInput = false
            }

            return correctInput
        },
        onSubmit () {
            var correctInput = this.checkInput()

            if (correctInput) {
                userApi.createUser(this.form.username, this.form.password,
                    this.form.firstname, this.form.lastname,
                    this.form.email, this.form.ltiJWT)
                    .then(_ => {
                        auth.login(this.form.username, this.form.password)
                            .then(_ => {
                                this.$emit('handleAction')
                            })
                            .catch(_ => {
                                this.$router.push({
                                    name: 'ErrorPage',
                                    params: {
                                        code: '511',
                                        message: 'Network authorization required',
                                        description: `Invalid credentials for logging in.
                                                      Please contact your system administrator.`
                                    }
                                })
                            })
                    })
                    .catch(error => {
                        this.$toasted.error(error.response.data.result + ': ' + error.response.data.description)
                    })
            }
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
    },
    mounted () {
        if (this.lti !== undefined) {
            this.form.username = this.lti.username
            this.form.firstname = this.lti.firstname
            this.form.lastname = this.lti.lastname
            this.form.email = this.lti.email
            this.form.ltiJWT = this.lti.ltiJWT
        }
    }
}
</script>
