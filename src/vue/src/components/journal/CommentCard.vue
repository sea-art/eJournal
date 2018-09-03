<!--
    Component that will show all the comments of a given entry and support
    the possibility to add comments when the right permissions are met.
-->
<template>
    <div>
        <div v-if="commentObject">
            <div v-for="(comment, index) in commentObject.entrycomments" class="comment-section" :key="index">
                <img class="profile-picture no-hover" :src="comment.author.picture">
                <b-card class="no-hover comment-card" :class="$root.getBorderClass($route.params.cID)">
                    <b-button v-if="$store.getters['user/uID'] == comment.author.uID" class="ml-2 delete-button float-right" @click="deleteComment(comment.ecID)">
                        <icon name="trash"/>
                        Delete
                    </b-button>
                    <b-button v-if="$store.getters['user/uID'] == comment.author.uID" class="ml-2 edit-button float-right">
                        <icon name="edit"/>
                        Edit
                    </b-button>
                    <div v-html="comment.text"/>
                    <hr/>
                    <b>{{ comment.author.first_name + ' ' + comment.author.last_name }}</b>
                    <span v-if="comment.published" class="timestamp">
                        {{ $root.beautifyDate(comment.timestamp) }}<br/>
                    </span>
                    <span v-else class="timestamp">
                        <icon name="hourglass-half" scale="0.8"/>
                        Will be published after grade<br/>
                    </span>
                </b-card>
            </div>
        </div>
        <div v-if="$hasPermission('can_comment_journal')" class="comment-section">
            <img class="profile-picture no-hover" :src="$store.getters['user/profilePicture']">
            <b-card class="no-hover new-comment">
                <text-editor
                    :id="'comment-text-editor'"
                    @content-update="tempComment = $event"
                />
                <!-- <b-textarea class="theme-input multi-form full-width" v-model="tempComment" placeholder="Write a comment" :class="$root.getBorderClass($route.params.cID)"/> -->
                <div class="d-flex full-width justify-content-end align-items-center">
                    <b-form-checkbox v-if="$hasPermission('can_grade_journal') && !entryGradePublished" v-model="publishAfterGrade">
                        Publish after grade
                    </b-form-checkbox>
                    <b-button class="send-button mt-2" @click="addComment">
                        <icon name="paper-plane"/>
                    </b-button>
                </div>
            </b-card>
        </div>
    </div>
</template>

<script>
import entryApi from '@/api/entry.js'
import icon from 'vue-awesome/components/Icon'
import textEditor from '@/components/assets/TextEditor.vue'

export default {
    props: {
        eID: {
            required: true
        },
        entryGradePublished: {
            type: Boolean,
            default: false
        }
    },
    components: {
        'text-editor': textEditor,
        icon
    },
    data () {
        return {
            tempComment: '',
            commentObject: null,
            publishAfterGrade: true,
            editCommentStatus: {}
        }
    },
    watch: {
        eID () {
            this.tempComment = ''
            entryApi.getEntryComments(this.eID)
                .then(data => { this.commentObject = data })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        entryGradePublished () {
            entryApi.getEntryComments(this.eID)
                .then(data => { this.commentObject = data })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        }
    },
    created () {
        this.getEntryComments()
    },
    methods: {
        getEntryComments () {
            entryApi.getEntryComments(this.eID)
                .then(data => { this.commentObject = data })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        setCommentEditStatus () {
            for (var comment in this.commentObject.entrycomments) {
                this.editCommentStatus[comment.ecID] = false
            }
        },
        addComment () {
            if (this.tempComment !== '') {
                entryApi.createEntryComment(this.eID, this.$store.getters['user/uID'], this.tempComment, this.entryGradePublished, this.publishAfterGrade)
                    .then(comment => {
                        // TODO Append comment rather than fire a get all entry comments request.
                        this.getEntryComments()
                        this.tempComment = ''
                    })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        },
        // editCommentStatus (ecID) {
        //
        // },
        // editComment (ecID) {
        //
        // },
        deleteComment (ecID) {
            if (confirm('Are you sure you want to delete this comment?')) {
                entryApi.deleteEntryComment(ecID)
                    // TODO Remove comment locally rather than firing a new request for all entry comments
                    .then(_ => { this.getEntryComments(this.eID) })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
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
        flex-wrap: wrap
    .card
        flex: 1 1 auto
        overflow: hidden
    .comment-card
        .card-body
            padding-bottom: 5px
        hr
            width: 120%
            margin-left: -10px !important
            border-color: $theme-dark-grey
            margin: 30px 0px 5px 0px
    .timestamp
        float: right
        font-family: 'Roboto Condensed', sans-serif
        color: grey
        svg
            fill: grey
</style>
