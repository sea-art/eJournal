<template>
    <b-card
        :class="$root.getBorderClass($route.params.uID)"
        class="no-hover multi-form"
    >
        <b-form @submit.prevent="changePassword()">
            <b-input
                name="username"
                autocomplete="username"
                hidden
            />
            <h2 class="field-heading">
                Current password
            </h2>
            <b-input
                v-model="oldPass"
                class="theme-input multi-form"
                type="password"
                placeholder="Current password"
                autocomplete="new-password"
            />
            <h2 class="field-heading">
                New password
            </h2>
            <b-input
                v-model="newPass"
                class="theme-input multi-form"
                type="password"
                placeholder="New password"
                autocomplete="new-password"
            />
            <h2 class="field-heading">
                Repeat new password
            </h2>
            <b-input
                v-model="newPassRepeat"
                class="theme-input multi-form"
                type="password"
                placeholder="Repeat new password"
                autocomplete="new-password"
            />
            <b-button
                type="submit"
                class="add-button float-right"
            >
                <icon name="save"/>
                Save
            </b-button>
        </b-form>
    </b-card>
</template>

<script>
import validation from '@/utils/validation.js'

import authAPI from '@/api/auth.js'

export default {
    data () {
        return {
            checkbox: false,
            oldPass: '',
            newPass: '',
            newPassRepeat: '',
        }
    },
    methods: {
        changePassword () {
            if (validation.validatePassword(this.newPass, this.newPassRepeat)) {
                authAPI.changePassword(this.newPass, this.oldPass, { responseSuccessToast: true })
            }
        },
        isChanged () {
            return (this.oldPass !== '' || this.newPass !== '' || this.newPassRepeat !== '')
        },
    },
}
</script>
