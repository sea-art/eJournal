<!--
    Component that will show all the comments of a given entry and support
    the possibility to add comments when the right permissions are met.
-->
<template>
    <div>
        <div v-if="commentObject">
            <div v-for="(comment, index) in commentObject" class="comment-section" :key="index">
                <img class="profile-picture no-hover" :src="comment.author.profile_picture">
                <b-card class="no-hover comment-card" :class="$root.getBorderClass($route.params.cID)">
                    <div v-if="!editCommentStatus[index]">
                        <b-button v-if="$store.getters['user/uID'] == comment.author.id" class="ml-2 delete-button float-right" @click="deleteComment(comment.id)">
                            <icon name="trash"/>
                            Delete
                        </b-button>
                        <b-button v-if="$store.getters['user/uID'] == comment.author.id" class="ml-2 change-button float-right" @click="editCommentView(index, true, comment.text)">
                            <icon name="edit"/>
                            Edit
                        </b-button>
                        <div v-html="comment.text"/>
                        <hr/>
                        <b>{{ comment.author.first_name + ' ' + comment.author.last_name }}</b>
                        <span v-if="comment.published && !comment.last_edited" class="timestamp">
                            {{ $root.beautifyDate(comment.timestamp) }}<br/>
                        </span>
                        <span v-else-if="comment.published && comment.last_edited" class="timestamp">
                            Last edited: {{ $root.beautifyDate(comment.last_edited) }}<br/>
                        </span>
                        <span v-else class="timestamp">
                            <icon name="hourglass-half" scale="0.8"/>
                            Will be published along with grade<br/>
                        </span>
                    </div>
                    <div v-else>
                        <text-editor
                            class="multi-form"
                            :id="'comment-text-editor-' + index"
                            :givenContent="editCommentTemp[index]"
                            @content-update="editCommentTemp[index] = $event"
                        />
                        <b-button v-if="$store.getters['user/uID'] == comment.author.id" class="multi-form delete-button" @click="editCommentView(index, false, '')">
                            <icon name="ban"/>
                            Cancel
                        </b-button>
                        <b-button v-if="$store.getters['user/uID'] == comment.author.id" class="ml-2 add-button float-right" @click="editComment(comment.id, index)">
                            <icon name="save"/>
                            Save
                        </b-button>
                    </div>
                </b-card>
            </div>
        </div>
        <div v-if="$hasPermission('can_comment_journal')" class="comment-section">
            <img class="profile-picture no-hover" :src="$store.getters['user/profilePicture']">
            <b-card class="no-hover new-comment">
                <text-editor
                    ref="comment-text-editor-ref"
                    :displayInline="true"
                    :basic="true"
                    :id="'comment-text-editor'"
                    @content-update="tempComment = $event"
                />
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
import icon from 'vue-awesome/components/Icon'
import textEditor from '@/components/assets/TextEditor.vue'

import commentAPI from '@/api/comment'

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
            editCommentStatus: [],
            editCommentTemp: []
        }
    },
    watch: {
        eID () {
            this.tempComment = ''
            this.getComments()
        },
        entryGradePublished () {
            this.getComments()
        }
    },
    created () {
        this.setComments()
    },
    methods: {
        setComments () {
            commentAPI.getFromEntry(this.eID)
                .then(comments => {
                    this.commentObject = comments
                    for (var i = 0; i < this.commentObject.length; i++) {
                        this.editCommentStatus.push(false)
                        this.editCommentTemp.push('')
                    }
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        getComments () {
            commentAPI.getFromEntry(this.eID)
                .then(comments => {
                    this.commentObject = comments
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        addComment () {
            if (this.tempComment !== '') {
                commentAPI.create({
                    entry_id: this.eID,
                    text: this.tempComment,
                    published: this.entryGradePublished || !this.publishAfterGrade
                })
                    .then(comment => {
                        // TODO Append comment rather than fire a get all entry comments request.
                        this.getComments()
                        this.tempComment = ''
                        this.$refs['comment-text-editor-ref'].clearContent()
                    })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        },
        editCommentView (index, status, text) {
            if (status) {
                this.$set(this.editCommentTemp, index, text)
            }

            this.$set(this.editCommentStatus, index, status)
        },
        editComment (cID, index) {
            this.$set(this.commentObject[index], 'text', this.editCommentTemp[index])
            this.$set(this.editCommentStatus, index, false)
            commentAPI.update(cID, {
                text: this.editCommentTemp[index]
            })
                .then(comment => { this.$set(this.commentObject, index, comment) })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        deleteComment (cID) {
            if (confirm('Are you sure you want to delete this comment?')) {
                commentAPI.delete(cID)
                    // TODO Remove comment locally rather than firing a new request for all entry comments
                    .then(_ => { this.getComments(this.eID) })
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
