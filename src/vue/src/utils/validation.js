import Vue from 'vue'

export default {
    validatePassword (password, password2) {
        if (password !== password2) {
            Vue.toasted.error('Passwords do not match!')
            return false
        }
        if (password.length < 8) {
            Vue.toasted.error('Password needs to contain at least 8 characters.')
            return false
        }
        if (password.toLowerCase() === password) {
            Vue.toasted.error('Password needs to contain at least 1 capital letter.')
            return false
        }
        let re = /[ !@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/
        if (!re.test(password)) {
            Vue.toasted.error('Password needs to contain a special character.')
            return false
        }

        return true
    }
}
