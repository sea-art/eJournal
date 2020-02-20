<template>
    <b-alert
        :show="showVersionAlert"
        dismissible
        @dismissed="hideVersionAlert"
    >
        A new version of eJournal has been released: <b>{{ version }}</b>.
        {{ message }}
        Read the changelog
        <a
            href="https://www.ejournal.app/changelog.html"
            target="_blank"
        >
            <b>here</b>
        </a>.
    </b-alert>
</template>
<script>
import preferencesAPI from '@/api/preferences'

export default {
    data () {
        return {
            version: CurrentRelease.version,
        }
    },
    computed: {
        showVersionAlert () {
            return this.message !== ''
                && this.$store.getters['preferences/hideVersionAlert'] !== this.version
                && this.$moment().diff(this.$moment(this.date), 'days') < 7
        },
    },
    methods: {
        hideVersionAlert () {
            preferencesAPI.update(this.$store.getters['user/uID'], { hide_version_alert: this.version })
                .then((preferences) => {
                    this.$store.commit('preferences/SET_HIDE_VERSION_ALERT', preferences.hide_version_alert)
                })
        },
    },
}

</script>
