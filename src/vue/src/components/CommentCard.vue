<template>
    <b-row>
        <b-col cols="2">
            <img class="profilePic" id="nav-profile-image" slot="button-content" src="../assets/unknown-profile.png">
        </b-col>
        <b-col cols="10">
            <b-card class="noHoverCard" :class="'pink-border'">
                <div v-if="EditSaveMode == 'Save'">
                    <b-textarea v-model="tempComment"></b-textarea><br><br>
                    <b-button @click="saveEdit">{{ EditSaveMode }}</b-button>
                    <b-button @click="cancel">Cancel</b-button>
                </div>
                <div v-else>
                    {{ comment }}<br><br>
                    <b-button @click="saveEdit">{{ EditSaveMode }}</b-button>
                </div>
            </b-card>
        </b-col>
    </b-row>
</template>

<script>
export default {
    props: ['comment'],

    data () {
        return {
            EditSaveMode: 'Edit',
            tempComment: this.comment
        }
    },

    methods: {
        saveEdit: function () {
            if (this.EditSaveMode === 'Save') {
                this.EditSaveMode = 'Edit'
                this.$emit('edit-comment', this.tempComment)
            } else {
                this.EditSaveMode = 'Save'
            }
        },

        cancel: function () {
            this.EditSaveMode = 'Edit'
            this.tempComment = this.comment
        }
    }
}
</script>
