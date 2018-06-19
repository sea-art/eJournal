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
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import Switch from '@/components/SwitchComponent.vue'
import userAPI from '@/api/user.js'

export default {
    props: ['gradeUpdate', 'commentUpdate'],
    components: {
        'toggle-switch': Switch
    },
    methods: {
        getGradeNotification (isActive) {
            userAPI.update_grade_notification(isActive)
                .then(isActive => { this.gradeUpdate = isActive })
        },
        getCommentNotification (isActive) {
            userAPI.update_grade_notification(isActive)
                .then(isActive => { this.commentUpdate = isActive })
        }
    }
}
</script>

<style>
</style>
