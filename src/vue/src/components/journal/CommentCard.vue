<!--
    Component that will show all the comments of a given entry and support
    the possibility to add comments when the right permissions are met.
-->
<template>
    <div>
        <div v-if="commentObject">
            <div
                v-for="(comment, index) in commentObject"
                :key="`comment-${eID}-${index}`"
                class="comment-section"
            >
                <img
                    :src="comment.author.profile_picture"
                    class="profile-picture-sm no-hover"
                />
                <b-card
                    :class="$root.getBorderClass($route.params.cID)"
                    class="no-hover comment-card"
                >
                    <div v-if="!editCommentStatus[index]">
                        <sandboxed-iframe :content="comment.text"/>
                        <hr class="full-width"/>
                        <b>{{ comment.author.full_name }}</b>
                        <icon
                            v-if="canEditComment(comment)"
                            name="trash"
                            class="float-right trash-icon"
                            @click.native="deleteComment(comment.id)"
                        />
                        <icon
                            v-if="canEditComment(comment)"
                            name="edit"
                            scale="1.07"
                            class="float-right ml-2 edit-icon"
                            @click.native="editCommentView(index, true, comment.text)"
                        />
                        <span
                            v-if="comment.published
                                && $root.beautifyDate(comment.last_edited)
                                    === $root.beautifyDate(comment.creation_date)"
                            class="timestamp"
                        >
                            {{ $root.beautifyDate(comment.creation_date) }}<br/>
                        </span>
                        <span
                            v-else-if="comment.published"
                            v-b-tooltip
                            :title="`Last edit by: ${comment.last_edited_by}`"
                            class="timestamp"
                        >
                            Last edited: {{ $root.beautifyDate(comment.last_edited) }}
                        </span>
                        <span
                            v-else
                            class="timestamp"
                        >
                            <icon
                                name="hourglass-half"
                                scale="0.8"
                            />
                            Will be published along with grade<br/>
                        </span>
                    </div>
                    <div v-else>
                        <text-editor
                            :id="'comment-text-editor-' + index"
                            v-model="editCommentTemp[index]"
                            :basic="true"
                            :footer="false"
                            class="multi-form"
                        />
                        <b-button
                            v-if="canEditComment(comment)"
                            class="multi-form delete-button"
                            @click="editCommentView(index, false, '')"
                        >
                            <icon name="ban"/>
                            Cancel
                        </b-button>
                        <b-button
                            v-if="canEditComment(comment)"
                            class="ml-2 add-button float-right"
                            @click="editComment(comment.id, index)"
                        >
                            <icon name="save"/>
                            Save
                        </b-button>
                    </div>
                </b-card>
            </div>
        </div>
        <div
            v-if="$hasPermission('can_comment')"
            class="comment-section"
        >
            <img
                :src="$store.getters['user/profilePicture']"
                class="profile-picture-sm no-hover"
            />
            <b-card
                :class="$root.getBorderClass($route.params.cID)"
                class="no-hover new-comment"
            >
                <text-editor
                    :id="'comment-text-editor'"
                    ref="comment-text-editor-ref"
                    v-model="tempComment"
                    :basic="true"
                    :footer="false"
                    placeholder="Type here to leave a comment"
                />
                <div class="d-flex full-width justify-content-end align-items-center">
                    <b-form-checkbox
                        v-if="$hasPermission('can_grade') && !entryGradePublished"
                        v-model="publishAfterGrade"
                    >
                        Publish after grade
                    </b-form-checkbox>
                    <b-button
                        class="mt-2"
                        @click="addComment"
                    >
                        <icon name="paper-plane"/>
                        Send
                    </b-button>
                </div>
            </b-card>
        </div>
    </div>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'
import sandboxedIframe from '@/components/assets/SandboxedIframe.vue'

import commentAPI from '@/api/comment.js'

export default {
    components: {
        textEditor,
        sandboxedIframe,
    },
    props: {
        eID: {
            required: true,
        },
        journal: {
            required: true,
        },
        entryGradePublished: {
            type: Boolean,
            default: false,
        },
    },
    data () {
        return {
            tempComment: '',
            commentObject: null,
            publishAfterGrade: true,
            editCommentStatus: [],
            editCommentTemp: [],
        }
    },
    watch: {
        eID () {
            this.tempComment = ''
            this.getComments()
        },
        entryGradePublished () {
            this.getComments()
        },
    },
    created () {
        this.setComments()
    },
    methods: {
        canEditComment (comment) {
            return this.$store.getters['user/uID'] === comment.author.id
                || (this.$hasPermission('can_edit_staff_comment') && comment.author.id !== this.journal.student.id)
        },
        setComments () {
            commentAPI.getFromEntry(this.eID)
                .then((comments) => {
                    this.commentObject = comments
                    for (let i = 0; i < this.commentObject.length; i++) {
                        this.editCommentStatus.push(false)
                        this.editCommentTemp.push('')
                    }
                })
        },
        getComments () {
            commentAPI.getFromEntry(this.eID)
                .then((comments) => { this.commentObject = comments })
        },
        addComment () {
            if (this.tempComment !== '') {
                commentAPI.create({
                    entry_id: this.eID,
                    text: this.tempComment,
                    published: this.entryGradePublished || !this.publishAfterGrade,
                })
                    .then((comment) => {
                        this.commentObject.push(comment)
                        for (let i = 0; i < this.commentObject.length; i++) {
                            this.editCommentStatus.push(false)
                            this.editCommentTemp.push('')
                        }
                        this.tempComment = ''
                        this.$refs['comment-text-editor-ref'].clearContent()
                    })
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
                text: this.editCommentTemp[index],
            })
                .then((comment) => { this.$set(this.commentObject, index, comment) })
        },
        deleteComment (cID) {
            if (window.confirm('Are you sure you want to delete this comment?')) {
                commentAPI.delete(cID)
                    .then(() => {
                        this.commentObject.forEach((comment, i) => {
                            if (comment.id === cID) {
                                this.commentObject.splice(i, 1)
                            }
                        })
                        this.commentObject.forEach(() => {
                            this.editCommentStatus.push(false)
                            this.editCommentTemp.push('')
                        })
                    })
            }
        },
    },
}
</script>

<style lang="sass">
.comment-section
    display: flex
    .profile-picture-sm
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
            .trash-icon, .edit-icon
                margin-top: 4px
                margin-left: 4px
</style>
