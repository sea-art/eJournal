<template>
    <div>
        <b-form @submit.prevent="onSubmit" @reset.prevent="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.username" placeholder="Username" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"  v-model="form.firstname" placeholder="Firstname" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"  v-model="form.lastname" placeholder="Lastname" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.password" placeholder="Password" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"  v-model="form.email" placeholder="Email" required/>
            <b-button class="float-right" type="reset">Reset</b-button>
            <b-button class="float-right" type="submit">Create</b-button>
        </b-form>
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
