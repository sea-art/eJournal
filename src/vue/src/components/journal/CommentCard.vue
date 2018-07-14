<!--
    Component that will show all the comments of a given entry and support
    the possibility to add comments when the right permissions are met.
-->
<template>
    <div>
        <div v-if="commentObject !== null">
            <div v-for="(comments, index) in commentObject.entrycomments" :key="index">
                <b-row>
                    <b-col cols="2">
                        <img class="profile-picture" :src="comments.author.picture">
                        <br><b>{{ comments.author.first_name + ' ' + comments.author.last_name }}</b>
                    </b-col>
                    <b-col cols="10">
                        <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
                            <span class="show-enters">{{ comments.text }}</span>
                        </b-card>
                    </b-col>
                </b-row>
            </div>
        </div>
        <div v-if="$root.canCommentJournal()">
            <b-row>
                <b-col cols="2">
                    <img class="profile-picture" :src="userData.picture">
                </b-col>
                <b-col cols="10">
                    <b-textarea v-model="tempComment" placeholder="Add your comment here" :class="$root.getBorderClass($route.params.cID)"></b-textarea><br>
                    <b-button @click="addComment">Add your comment</b-button>
                </b-col>
            </b-row>
        </div>
    </div>
</template>

<script>
import userApi from '@/api/user.js'
import entryApi from '@/api/entry.js'

export default {
    props: ['eID'],
    data () {
        return {
            tempComment: '',
            userData: '',
            commentObject: null
        }
    },
    watch: {
        eID: function () {
            this.tempComment = ''
            entryApi.getEntryComments(this.eID).then(response => { this.commentObject = response })
        }
    },
    created () {
        this.getAuthorID()
        this.getEntryComments()
    },
    methods: {
        getAuthorID: function () {
            userApi.getOwnUserData()
                .then(response => { this.userData = response })
        },
        getEntryComments: function () {
            entryApi.getEntryComments(this.eID).then(response => { this.commentObject = response })
        },
        addComment: function () {
            if (this.tempComment !== '') {
                entryApi.createEntryComment(this.eID, this.userData.uID, this.tempComment)
                this.commentObject.entrycomments.push({
                    entrtyID: this.eID,
                    author: {
                        first_name: this.userData.first_name,
                        last_name: this.userData.last_name,
                        picture: this.userData.picture
                    },
                    text: this.tempComment
                })
                this.tempComment = ''
            }
        }
    }
}
</script>
