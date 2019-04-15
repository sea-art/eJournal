<template>
    <content-single-column>
        <h1><span>Welcome to {{ this.name ? this.name : 'eJournal' }}!</span></h1><br/>
        <h4 class="multi-form"><span>Let's get started</span></h4>
        <login-form @handleAction="handleLoginSucces"/>
        <h4 class="multi-form mt-4"><span>Want to use eJournal in your education?</span></h4>
        <div class="mb-5">
            eJournal is a blended learning application that provides an easy to manage graded journal system for teachers and students. It seamlessly connects to your <i>learning management system</i> (LMS) via LTI, allowing for automatic grade passback and simple setup.
            Do you want to use eJournal in your education? Do not hesitate to contact us!
            <div class="text-right">
                <b-button class="big-button-text" href="https://www.ejournal.app" target="_blank">
                    <icon name="globe" scale="1.3"/>
                    Website
                </b-button>
            </div>
        </div>

        <h4 class="multi-form mt-4"><span>eJournal is open source software</span></h4>
        <div class="mb-5">
            eJournal is an open source project. This means that you have the right to see the source code and many more.
            You can find this and more information including instructions for deployment on our GitHub repository.
            <div class="text-right">
                <b-button class="big-button-text" href="https://github.com/eJourn-al/eJournal/" target="_blank">
                    <icon name="github" scale="1.3"/>
                    GitHub
                </b-button>
            </div>
        </div>
        <custom-footer style="clear:both"/>
    </content-single-column>
</template>
<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import customFooter from '@/components/assets/Footer.vue'
import icon from 'vue-awesome/components/Icon'
import loginForm from '@/components/account/LoginForm.vue'
import routerConstraints from '@/utils/constants/router_constraints.js'

import instanceAPI from '@/api/instance'

export default {
    name: 'Guest',
    components: {
        icon,
        contentSingleColumn,
        customFooter,
        loginForm
    },
    data () {
        return {
            name: null,
            username: '',
            password: ''
        }
    },
    created () {
        instanceAPI.get()
            .then(instance => {
                this.name = instance.name
            })
    },
    methods: {
        handleLoginSucces () {
            if (this.$root.previousPage === null || this.$root.previousPage.name === null ||
                this.$root.previousPage.name === 'Logout' ||
                routerConstraints.PERMISSIONLESS_CONTENT.has(this.$root.previousPage.name)) {
                this.$router.push({name: 'Home'})
            }

            this.$router.push({name: this.$root.previousPage.name, params: this.$root.previousPage.params})
        }
    }
}
</script>
