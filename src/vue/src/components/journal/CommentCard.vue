<!--
    Component that will show all the comments of a given entry and support
    the possibility to add comments when the right permissions are met.
-->
<template>
    <div>
        <div v-if="commentObject">
            <div v-for="(comment, index) in commentObject.entrycomments" class="comment-section" :key="index">

                <img class="profile-picture no-hover" :src="comment.author.picture">
                <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
                    <b-button class="delete-button float-right" @click="deleteComment(comment.ecID)">
                        <icon name="trash"/>
                        Delete
                    </b-button>
                    <b>{{ comment.author.first_name + ' ' + comment.author.last_name }}</b><br/>
                    <span class="show-enters">{{ comment.text }}</span>
                </b-card>
            </div>
        </div>
        <div v-if="$root.canCommentJournal()" class="comment-section">
            <img class="profile-picture no-hover" :src="userData.picture">
            <b-card class="no-hover new-comment">
                <b-textarea class="theme-input" v-model="tempComment" placeholder="Write a comment" :class="$root.getBorderClass($route.params.cID)"/>
                <b-button class="send-button" @click="addComment">
                    <icon name="paper-plane"/>
                </b-button>
            </b-card>
        </div>
    </div>
</template>

<script>
import userApi from '@/api/user.js'
import entryApi from '@/api/entry.js'
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['eID'],
    components: {
        icon
    },
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
        getAuthorID () {
            userApi.getOwnUserData()
                .then(response => { this.userData = response })
        },
        getEntryComments () {
            entryApi.getEntryComments(this.eID)
                .then(response => {
                    this.commentObject = response
                })
        },
        addComment () {
            if (this.tempComment !== '') {
                entryApi.createEntryComment(this.eID, this.userData.uID, this.tempComment)
                    .then (_ => {
                        this.getEntryComments()
                        this.tempComment = ''
                    })
                    .catch(_ => { this.$toasted.error('Something went wrong whilst posting your comment, please try again!') })
            }
        },
        deleteComment (ecID) {
            if (confirm('Are you sure you want to delete this comment?')) {
                entryApi.deleteEntryComment(ecID)
                    .then(_ => { this.getEntryComments(this.eID) })
                    .catch(_ => { this.$toasted.error('Something went wrong whilst deleting the comment, please try again!') })
            }
        }
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
.comment-section
    display: flex
    transition: all 0.6s cubic-bezier(.25,.8,.25,1)
    .profile-picture
        margin: 0px 12px
        display: inline
    .new-comment .card-body
        display: flex
    .card, textarea
        flex: 1 1 auto
    textarea
        margin-right: 10px
</style>
