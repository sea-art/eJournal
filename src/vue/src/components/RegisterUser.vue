<template>
    <div>
        <b-form @submit="onSubmit" @reset="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0" v-model="form.username" placeholder="Username" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0" v-model="form.password" placeholder="Password" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0"  v-model="form.email" placeholder="Email" required/>
            <b-form-select :options="instutes" v-model="selected" required></b-form-select>
            <b-button type="submit" variant="primary">Register</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
    </div>
</template>

<script>
export default {
    data () {
        return {
            instutes: [
                {
                    text: 'Select the applicable institute',
                    value: null
                },
                'Universiteit van Amsterdam (UvA)'
            ],
            
            form: {
                selected: null,
                institude: '',
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
