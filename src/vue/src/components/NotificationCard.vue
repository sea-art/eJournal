<template>
    <b-container>
        <b-row>
            <h8>Notification-emails</h8><br/>
        </b-row>
        <b-row>
            <b-col cols="3">
                <p class="profile-notification">Grade updates</p>
                <p class="profile-notification">comments</p>
            </b-col>
            <b-col class="notification-body" cols="3">
                <toggle-switch :isActive="gradeUpdate"></toggle-switch>
                <toggle-switch></toggle-switch>
                {{gradeUpdate}}
            </b-col>
            <b-col cols="6"></b-col>
        </b-row>
    </b-container>
</template>

<script>
import Switch from '@/components/switchComponent.vue'

export default {
    components: {
        // 'switches': Switches,
        'toggle-switch': Switch
    },
    data () {
        return {
            gradeUpdate: false
        }
    }
}
</script>

<style>
.notifcatian {line-height: 10px;}

.col-3 {padding-left: 0px;}
</style>
