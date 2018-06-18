<template>
    <b-container>
        <b-row>
            <p class="profile-title">Notification-emails</p><br/>
        </b-row>
        <b-row>
            <b-col class="profile-col" cols="4">
                <p class="profile-notification">Grade updates</p>
            </b-col>
            <b-col cols="6">
                <toggle-switch :isActive="gradeUpdate"
                               @parentActive="getGradeNotification">
                </toggle-switch>
                <!-- {{gradeUpdate}} -->
            </b-col>
        </b-row>
        <b-row>
            <b-col class="profile-col" cols="4">
                <p class="profile-notification">Comments</p>
            </b-col>
            <b-col cols="6">
                <toggle-switch :isActive="commentUpdate"
                               @parentActive="getCommentNotification">
                </toggle-switch>
                <!-- {{commentUpdate}} -->
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import Switch from '@/components/SwitchComponent.vue'

export default {
    components: {
        'toggle-switch': Switch
    },
    data () {
        return {
            gradeUpdate: true,
            commentUpdate: false
        }
    },
    methods: {
        getGradeNotification (isActive) {
            this.gradeUpdate = isActive
        },
        getCommentNotification (isActive) {
            this.commentUpdate = isActive
        }
    }
}
</script>

<style>
</style>
