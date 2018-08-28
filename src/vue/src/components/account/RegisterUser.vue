<template>
    <div>
        <b-card class="blue-border no-hover card-last-elem-button">
            <b-form @submit.prevent="onSubmit" @reset.prevent="onReset">
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.username" placeholder="Username" required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.firstname" placeholder="First name" required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.lastname" placeholder="Last name" required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.password" type="password" placeholder="Password" required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.password2" type="password" placeholder="Password (again)" required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.email" placeholder="Email" required/>
                <b-button class="float-left change-button multi-form" type="reset">
                    <icon name="undo"/>
                    Reset
                </b-button>
                <b-button class="float-right multi-form" type="submit">
                    <icon name="user-plus"/>
                    Register
                </b-button>
            </b-form>
        </b-card>
    </div>
</template>

<script>
import authAPI from '@/api/auth'
import icon from 'vue-awesome/components/Icon'
import validation from '@/utils/validation.js'

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
        onSubmit () {
            if (validation.validatePassword(this.form.password, this.form.password2) && validation.validateEmail(this.form.email)) {
                authAPI.register(this.form.username, this.form.password, this.form.firstname, this.form.lastname,
                    this.form.email, this.form.ltiJWT)
                    .then(_ => {
                        if (!this.lti) {
                            this.$toasted.success('Registration successfull! Please follow the instructions sent to ' + this.email +
                                                  ' to confirm your email address.')
                        }
                        authAPI.login(this.form.username, this.form.password)
                            .then(_ => { this.$emit('handleAction') })
                            .catch(_ => { this.$toasted.error('Error logging in with your newly created account, please contact a system administrator or try registering again.') })
                    })
                    .catch(error => {
                        this.$toasted.error(error.response.data.description)
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
    },
    components: {
        icon
    }
}
</script>
