<template>
    <div>
        {{authorID}}
        <div v-for="(comment, index) in comments" :key="index">
            <b-row>
                <b-col cols="2">
                    <img class="profilePic" id="nav-profile-image" slot="button-content" src="../assets/unknown-profile.png">
                    {{ comment.person }}
                </b-col>
                <b-col cols="10">
                    <b-card class="no-hover" :class="'pink-border'">
                        {{ comment.message }}
                    </b-card>
                </b-col>
            </b-row>
        </div>
        <b-row>
            <b-col cols="2">
            </b-col>
            <b-col cols="10">
                <b-textarea v-model="tempComment" placeholder="Add your beautiful comment here"></b-textarea><br>
                <b-button @click="addComment">Add your comment</b-button>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import userApi from '@/api/user.js'

export default {
    props: ['comments', 'person', 'eID'],

    data () {
        return {
            newComments: this.comments,
            tempComment: '',
            authorID: ''
        }
    },
    watch: {
        eID: function () {
            this.newComments = this.comments
            this.tempComment = ''
        }
    },
    created () {
        this.getAuthorID()
    },
    methods: {
        getAuthorID: function () {
            userApi.getOwnUserData()
                .catch(_ => alert('Error while loading in user data.'))
                .then(response => { this.authorID = response })
        },
        addComment: function () {
            if (this.tempComment !== '') {
                this.newComments.push({
                    message: this.tempComment,
                    person: this.person
                })
                this.$emit('new-comments', this.tempComment)
                this.tempComment = ''
            }
        }
    }
}
</script>
