<template>
    <b-row>
        <b-col cols="12">
            <h2 class="mb-2">Email notification</h2>
        </b-col>
        <b-col cols="4">
            <span>Grade updates</span>
        </b-col>
        <b-col cols="8">
            <toggle-switch :isActive="gradeUpdate"
                           @parentActive="getGradeNotification">
            </toggle-switch>
        </b-col>
        <b-col cols="4">
            <span>Comments</span>
        </b-col>
        <b-col cols="8">
            <toggle-switch :isActive="commentUpdate"
                           @parentActive="getCommentNotification">
            </toggle-switch>
        </b-col>
    </b-row>
</template>

<script>
import Switch from '@/components/assets/SwitchComponent.vue'
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
