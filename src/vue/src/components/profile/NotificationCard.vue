<template>
    <b-row>
        <b-col cols="12">
            <h2 class="mb-2">Email notifications</h2>
        </b-col>
        <b-col cols="4">
            Grade updates
        </b-col>
        <b-col cols="8">
            <toggle-switch :isActive="$store.getters['preferences/gradeNotifications']"
                           @parentActive="getGradeNotification">
            </toggle-switch>
        </b-col>
        <b-col cols="4">
            Comments
        </b-col>
        <b-col cols="8">
            <toggle-switch :isActive="$store.getters['preferences/commentNotifications']"
                           @parentActive="getCommentNotification">
            </toggle-switch>
        </b-col>
        <b-col cols="4">
            Tutorial
        </b-col>
        <b-col cols="8">
            <toggle-switch :isActive="$store.getters['preferences/showFormatTutorial']"
                           @parentActive="getFormat">
            </toggle-switch>
        </b-col>
    </b-row>
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
            preferencesAPI.update(0, {grade_notifications: isActive}, {customSuccessToast: 'Grade notification setting updated successfully.'})
                .then(preferences => { this.$store.commit('preferences/SET_GRADE_NOTIFICATION', preferences.grade_notifications) })
        },
        getCommentNotification (isActive) {
            preferencesAPI.update(0, {comment_notifications: isActive}, {customSuccessToast: 'Comment notification setting updated successfully.'})
                .then(preferences => { this.$store.commit('preferences/SET_COMMENT_NOTIFICATION', preferences.comment_notifications) })
        },
        getFormat (isActive) {
            preferencesAPI.update(0, {show_format_tutorial: isActive}, {customSuccessToast: 'Format setting updated successfully.'})
                .then(preferences => { this.$store.commit('preferences/SET_FORMAT_TUTORIAL', preferences.show_format_tutorial) })
        }
    }
}
</script>
