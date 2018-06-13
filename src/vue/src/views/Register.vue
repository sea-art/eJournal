<template>
    <b-form @submit="onSubmit" @reset="onReset">
        <h1>Register (Temporary page)</h1>
        <b-input class="mb-2 mr-sm-2 mb-sm-0" id="registerFormInputUsername" v-model="form.username" placeholder="Username"/>
        <b-input class="mb-2 mr-sm-2 mb-sm-0" id="registerFormInputPassword" v-model="form.password" placeholder="Password"/>
        <b-input class="mb-2 mr-sm-2 mb-sm-0" id="registerFormInputEmail" v-model="form.email" placeholder="Email"/>
        <b-form-select id="registerFormSelectInstitute" :options="instutes" v-model="selected" required></b-form-select>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
</template>

<script>
export default {
    data () {
        return {
            selected: null,
            form: {
                username: '',
                password: '',
                email: ''
            },
            instutes: [
                { text: 'Select the applicable institute', value: null },
                'Universiteit van Amsterdam (UvA)']
        }
    },
    methods: {
        onSubmit (evt) {
            alert('Submit')
        },
        onReset (evt) {
            evt.preventDefault()
            /* Reset our form values */
            this.form.email = ''
            this.form.password = ''
            this.form.username = ''
            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    }
}
</script>
