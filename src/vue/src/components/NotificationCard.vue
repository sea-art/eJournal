<template>
    <b-container>
        <b-row>
            <span class="profile-title">Notification-emails</span><br/>
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
            {{gradeUpdate}}
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
            <!-- {{commentUpdate}} -->
        </b-row>
    </b-container>
</template>

<script>
import Switch from '@/components/SwitchComponent.vue'
import userAPI from '@/api/user.js'

export default {
    // props: ['gradeUpdate', 'commentUpdate'],
    components: {
        'toggle-switch': Switch
    },
    data () {
        return {
            'profile': {},
            'gradeUpdate': null,
            'commentUpdate': null
        }
    },
    created () {
        userAPI.get_own_user_data().then(user => {
            this.profile = user
            this.gradeUpdate = this.profile.grade_notifications
            this.commentUpdate = this.profile.comment_notifications
        })
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
