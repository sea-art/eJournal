<template>
    <content-single-column>
        <h1>Welcome to eJournal!</h1>
        <b-card class="no-hover blue-border">
            <h2 class="multi-form">Let's get started</h2>
            <b-row>
                <b-col md="6">
                    <b-card class="no-hover full-height">
                        <b-button class="add-button full-width" :to="{ name: 'Register' }">
                            <h2 class="lti-button-text">
                                <icon name="user-plus" scale="1.5"/>
                                Register
                            </h2>
                        </b-button>
                        <hr/>
                        If this is the first time you are here, click the button above to register a new account.
                        This user however won't be linked to any course. Contact the teacher or connect you account with Canvas to connect to a course.
                    </b-card>
                </b-col>
                <b-col md="6">
                    <b-card class="no-hover full-height">
                        <b-button class="default-button full-width" :to="{ name: 'Login' }">
                            <h2 class="lti-button-text">
                                <icon name="sign-in" scale="1.5"/>
                                Login
                            </h2>
                        </b-button>
                        <hr/>
                        If you already have an account on eJournal, click the button above to login.
                    </b-card>
                </b-col>
            </b-row>
        </b-card>
        <b-card class="no-hover blue-border">
            <h2 class="multi-form">Want to use eJournal for your organisation?</h2>
            <b-row>
                <b-col md="6">
                    <b-card class="no-hover full-height">
                        <b-button class="change-button full-width" href="mailto:contact@ejourn.al">
                            <h2 class="lti-button-text">
                                <icon name="comments" scale="1.5"/>
                                Contact
                            </h2>
                        </b-button>
                        <hr/>
                        If you want to use eJournal for an organisation, or just want to get some information first, contact us!
                    </b-card>
                </b-col>
                <b-col md="6">
                    <b-card class="no-hover full-height">
                        <b-button class="btn full-width" href="https://github.com/eJourn-al/eJournal/">
                            <h2 class="lti-button-text">
                                <icon name="github" scale="1.5"/>
                                GitHub
                            </h2>
                        </b-button>
                        <hr/>
                        This is an open source project. This means you can also deploy it yourself to try it out.
                        The button above will bring you to the Github repository where there are further instructions on how to deploy.
                    </b-card>
                </b-col>
            </b-row>
        </b-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'Guest',
    components: {
        icon,
        'content-single-column': contentSingleColumn
    }
}
</script>
