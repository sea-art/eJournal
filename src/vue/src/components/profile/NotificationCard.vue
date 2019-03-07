<template>
    <div class="multi-form">
        <h2 class="mb-2">Email notifications</h2>
        <!-- TODO: enable once comment and grade notifications available - <toggle-switch
            class="float-right"
            :isActive="$store.getters['preferences/gradeNotifications']"
            @parentActive="getGradeNotification"/>
        <h2 class="field-heading multi-form">Grade updates</h2>
        <toggle-switch
            class="float-right"
            :isActive="$store.getters['preferences/commentNotifications']"
            @parentActive="getCommentNotification"/>
        <h2 class="field-heading multi-form">Comments</h2> -->
        <toggle-switch
            class="float-right"
            :isActive="$store.getters['preferences/upcomingDeadlineNotifications']"
            @parentActive="getUpcomingDeadlineNotification"/>
        <h2 class="field-heading multi-form">Upcoming deadlines</h2>
    </div>
</template>

<script>
import Switch from '@/components/assets/SwitchComponent.vue'
import preferencesAPI from '@/api/preferences'

export default {
    props: ['userData'],
    components: {
        'toggle-switch': Switch
    },
    methods: {
        getGradeNotification (isActive) {
            preferencesAPI.update(this.$store.getters['user/uID'], {grade_notifications: isActive}, {customSuccessToast: 'Grade notification setting updated successfully.'})
                .then(preferences => { this.$store.commit('preferences/SET_GRADE_NOTIFICATION', preferences.grade_notifications) })
        },
        getCommentNotification (isActive) {
            preferencesAPI.update(this.$store.getters['user/uID'], {comment_notifications: isActive}, {customSuccessToast: 'Comment notification setting updated successfully.'})
                .then(preferences => { this.$store.commit('preferences/SET_COMMENT_NOTIFICATION', preferences.comment_notifications) })
        },
        getUpcomingDeadlineNotification (isActive) {
            preferencesAPI.update(this.$store.getters['user/uID'], {upcoming_deadline_notifications: isActive}, {customSuccessToast: 'Upcoming deadline notification setting updated successfully.'})
                .then(preferences => { this.$store.commit('preferences/SET_UPCOMING_DEADLINE_NOTIFICATION', preferences.upcoming_deadline_notifications) })
        }
    }
}
</script>
