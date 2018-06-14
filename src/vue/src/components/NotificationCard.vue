<template>
    <b-container>
        <b-row>
            <h8>Notification-emails</h8><br/>
        </b-row>
        <b-row>
            <b-col cols="3">
                <p class="profile">Grade updates</p>
                <p class="profile">comments</p>
            </b-col>
            <b-col cols="3">
                <switches class="notifcation" v-model="disabled" theme="bulma" color="red"></switches><br/>
                <switches class="notifcation" v-model="enabled" theme="bulma" color="red"></switches>

                <toggle-switch v-model="checkbox">toggle</toggle-switch>
            </b-col>
            <b-col cols="6"></b-col>
        </b-row>
    </b-container>
</template>

<script>
import Switches from '../../node_modules/vue-switches/src/switches.vue';
import Switch from '@/components/switchComponent.vue';

export default {
    components: {
        'switches': Switches,
        'toggle-switch': Switch
    },
    data() {
        return {
            checkbox: false
        }
    }

}
</script>

<style>
.notifcatian {
        line-height: 10px;
}
</style>
