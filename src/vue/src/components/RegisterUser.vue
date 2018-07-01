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
                <b-button class="float-right" type="reset">Reset</b-button>
                <b-button class="float-right" type="submit">Register</b-button>
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

            /* Validate the password. */
            var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/
            if (!re.test(String(this.form.password))) {
                this.$toasted.error('The given password does not match the criteria!')
                correctInput = false
            }
            if (this.form.password !== this.form.password2) {
                this.$toasted.error('The given passwords do not match!')
                correctInput = false
            }

            /* Validate the email. */
            re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            if (!re.test(String(this.form.email).toLowerCase())) {
                this.$toasted.error('The given email is incorrect!')
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
                    .catch(_ => {
                        this.$router.push({
                            name: 'ErrorPage',
                            params: {
                                code: '500',
                                message: 'Internal Server Error',
                                description: `Could not create user. Please contact
                                              your system administrator.`
                            }
                        })
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
