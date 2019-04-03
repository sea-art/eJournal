<template>
    <content-single-column>
        <h1><span>Welcome to {{ this.name ? this.name : 'eJournal' }}!</span></h1><br/>
        <h4 class="multi-form"><span>Let's get started</span></h4>
        <login-form @handleAction="handleLoginSucces"/>
        <h4 class="multi-form mt-4"><span>Want to use eJournal in your education?</span></h4>
        <b-card class="no-hover">
            <b>eJournal is a blended learning application that provides an easy to manage graded journal system for teachers and students. It seamlessly connects to your <i>learning management system</i> (LMS) via LTI, allowing for automatic grade passback and simple setup.</b>
            Do you want to use eJournal in your education? Do not hesitate to contact us!

            <hr/>
            <div class="text-center multi-form">
                <b-button class="change-button big-button-text" href="mailto:contact@ejourn.al" target="_blank">
                    <icon name="envelope" class="shift-up-2" scale="1.5"/>
                    Email
                </b-button>
                <b-button class="blue-button big-button-text" href="https://www.linkedin.com/company/eJourn-al" target="_blank">
                    <icon name="linkedin" class="shift-up-2" scale="1.5"/>
                    LinkedIn
                </b-button>
            </div>
        </b-card>

        <h4 class="multi-form mt-4"><span>eJournal is open source software</span></h4>
        <b-card class="no-hover">
            <b>eJournal is an open source project.</b> This means you are free to deploy it yourself to try it out.
            You can find the source code and more information including instructions for deployment on our GitHub repository below.
            <hr/>
            <div class="text-center multi-form">
                <b-button class="black-button big-button-text" href="https://github.com/eJourn-al/eJournal/" target="_blank">
                    <icon name="github" scale="1.5"/>
                    GitHub
                </b-button>
            </div>
        </b-card>
        <custom-footer/>
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
