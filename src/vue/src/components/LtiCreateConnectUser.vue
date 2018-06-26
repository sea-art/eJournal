<template>
    <div slot="main-content-column">
        <p class="lti-intro-text">You came here from canvas with an unknown
            user account. Do you want to create a new user on Logboek,
            or connect to an existing one?</p>
        <b-row align-h="center">
            <b-button class="lti-button-option" @click="showModal('createCourseRef')">
                <h2 class="lti-button-text">Create new course</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="lti-button-option" @click="showModal('connectCourseRef')">
                <h2 class="lti-button-text">Connect to existing course</h2>
            </b-button>
        </b-row>

        <b-modal
            slot="main-content-column"
            ref="createCourseRef"
            title="Create course"
            size="lg"
            hide-footer>
                <create-course @handleAction="handleCreation" :lti="lti"/>
        </b-modal>

        <b-modal
            slot="main-content-column"
            ref="connectCourseRef"
            title="Connect course"
            size="lg"
            hide-footer>
                <connect-course @handleAction="handleConnected" :lti="lti"/>
        </b-modal>
    </div>
</template>

<script>
export default {

}
</script>
