<template>
    <b-container no-gutters>
        <b-row>
            <h3 class="profile-title">Email notification</h3><br/>
        </b-row>
        <b-row>
            <b-col class="profile-col" cols="4">
                <span class="profile-notification">Grade updates</span>
            </b-col>
            <b-col cols="6">
                <toggle-switch :isActive="gradeUpdate"
                               @parentActive="getGradeNotification">
                </toggle-switch>
            </b-col>
        </b-row>
        <b-row>
            <b-col class="profile-col" cols="4">
                <span class="profile-notification">Comments</span>
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
            userAPI.updateGradeNotification(isActive)
                .then(isActive => { this.gradeUpdate = isActive })
        },
        getCommentNotification (isActive) {
            userAPI.updateCommentNotification(isActive)
                .then(isActive => { this.commentUpdate = isActive })
        }
    }
}
</script>

<style>
</style>
