<template>
    <content-single-column>
        <h1><span>Welcome to {{ name ? name : 'eJournal' }}</span></h1><br/>
        <h4 class="multi-form">
            <span>Let's get started</span>
        </h4>
        <login-form @handleAction="handleLoginSucces"/>
        <h4 class="multi-form mt-4">
            <span>Want to use eJournal in your education?</span>
        </h4>
        <p>
            eJournal is a blended learning web application that provides an easy to manage graded journal system
            focused on education. Curious what eJournal has to offer for your education?
        </p>
        <b-button href="#feature-section">
            <icon name="play"/>
            Learn more
        </b-button>
        <b-button
            href="mailto:contact@ejournal.app?subject=I%20would%20like%20to%20know%20more%20about%20eJournal!"
            class="change-button ml-2"
        >
            <icon name="desktop"/>
            Request a demo
        </b-button>
        <custom-footer style="clear:both"/>
    </content-single-column>
</template>
<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import customFooter from '@/components/assets/Footer.vue'
import loginForm from '@/components/account/LoginForm.vue'
import routerConstraints from '@/utils/constants/router_constraints.js'

import instanceAPI from '@/api/instance.js'

export default {
    name: 'Guest',
    components: {
        contentSingleColumn,
        customFooter,
        loginForm,
    },
    data () {
        return {
            name: null,
            username: '',
            password: '',
        }
    },
    created () {
        instanceAPI.get()
            .then((instance) => {
                this.name = instance.name
            })
    },
    methods: {
        handleLoginSucces () {
            if (this.$root.previousPage === null || this.$root.previousPage.name === null
                || this.$root.previousPage.name === 'Logout'
                || routerConstraints.PERMISSIONLESS_CONTENT.has(this.$root.previousPage.name)) {
                this.$router.push({ name: 'Home' })
            }

            this.$router.push({ name: this.$root.previousPage.name, params: this.$root.previousPage.params })
        },
    },
}
</script>
