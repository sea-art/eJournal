<!--
    Component that will show all the comments of a given entry and support
    the possibility to add comments when the right permissions are met.
-->
<template>
    <div>
        <div v-if="commentObject !== null">
            <div v-for="(comment, index) in commentObject.entrycomments" class="comment-section" :key="index">

                <img class="profile-picture no-hover" :src="comment.author.picture">
                <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
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

<style lang="sass">
@import '~sass/modules/colors.sass'
.comment-section
    display: flex
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
