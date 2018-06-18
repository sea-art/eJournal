<template>
    <b-row>
        <b-col cols="2">
            <img class="profilePic" id="nav-profile-image" slot="button-content" src="../assets/unknown-profile.png">

        </b-col>
        <b-col cols="10">
            <b-card>
                <div v-if="saveEditMode == 'Save'">
                    <b-textarea v-model="tempComment"></b-textarea><br><br>
                    <b-button @click="saveEdit">{{ saveEditMode }} </b-button>
                    <b-button @click="cancel">Cancel</b-button>
                </div>
                <div v-else>
                    {{ tempComment }}
                    <b-button @click="saveEdit">{{ saveEditMode }} </b-button>
                </div>

            </b-card>
        </b-col>
    </b-row>
</template>

<script>
export default {
    /* Variables that are needed to fill in the template. */
    props: ['comment'],

    data () {
        return {
            saveEditMode: 'Edit',
            tempComment: this.comment
        }
    },

    methods: {
        saveEdit: function () {
            if (this.saveEditMode === 'Save') {
                this.saveEditMode = 'Edit'
                // this.$emit('edit-comment', this.tempComment)
            } else {
                this.tempbox1 = this.tempComment
                this.saveEditMode = 'Save'
            }
        },

        cancel: function () {
            this.saveEditMode = 'Edit'
        }
    }
}
