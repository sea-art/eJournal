<!--
    Loads a filled in template of an entry and the corresponding
    comments. The teacher tools will also be loaded if the user has the
    right permissions.
-->
<template>
    <div v-if="entryNode.entry !== null">
        <b-card
            class="no-hover entry-card-teacher"
            :class="$root.getBorderClass($route.params.cID)"
        >
            <div>
                <div
                    v-if="$hasPermission('can_grade')"
                    class="grade-section shadow sticky"
                >
                    <b-form-input
                        v-model="grade"
                        type="number"
                        class="theme-input"
                        size="2"
                        autofocus
                        placeholder="0"
                        min="0.0"
                    />
                    <b-form-checkbox
                        v-model="published"
                        inline
                        fieldValue="true"
                        uncheckedFieldValue="false"
                        data-toggle="tooltip"
                        title="Show grade to student"
                    >
                        Published
                    </b-form-checkbox>
                    <b-button
                        class="add-button"
                        @click="commitGrade"
                    >
                        <icon
                            name="save"
                            scale="1"
                        />
                        Save grade
                    </b-button>
                </div>
                <div
                    v-else-if="tempNode.entry.published"
                    class="grade-section grade shadow"
                >
                    {{ entryNode.entry.grade }}
                </div>
                <div
                    v-else
                    class="grade-section grade shadow"
                >
                    <icon name="hourglass-half"/>
                </div>

                <h2 class="mb-2">
                    {{ entryNode.entry.template.name }}
                </h2>
                <entry-fields
                    :nodeID="entryNode.nID"
                    :template="entryNode.entry.template"
                    :completeContent="completeContent"
                    :displayMode="true"
                    :authorUID="$parent.journal.student.id"
                    :entryID="entryNode.entry.id"
                />
            </div>
            <hr class="full-width"/>
            <div class="timestamp">
                <span
                    v-if="$root.beautifyDate(entryNode.entry.last_edited)
                        === $root.beautifyDate(entryNode.entry.creation_date)"
                >
                    Submitted on: {{ $root.beautifyDate(entryNode.entry.creation_date) }}
                </span>
                <span v-else>
                    Last edited: {{ $root.beautifyDate(entryNode.entry.last_edited) }}
                </span>
                <b-badge
                    v-if="entryNode.due_date && new Date(entryNode.due_date) < new Date(entryNode.entry.last_edited)"
                    class="late-submission-badge"
                >
                    LATE
                </b-badge>
            </div>
        </b-card>

        <comment-card
            :eID="entryNode.entry.id"
            :entryGradePublished="entryNode.entry.published"
            :journal="journal"
        />
    </div>
    <b-card
        v-else
        :class="$root.getBorderClass($route.params.cID)"
        class="no-hover"
    >
        <h2 class="mb-2">
            {{ entryNode.template.name }}
        </h2>
        <b>No submission for this student</b>
    </b-card>
</template>

<script>
import commentCard from '@/components/journal/CommentCard.vue'
import entryFields from '@/components/entry/EntryFields.vue'
import entryAPI from '@/api/entry.js'

export default {
    components: {
        commentCard,
        entryFields,
    },
    props: ['entryNode', 'journal'],
    data () {
        return {
            tempNode: this.entryNode,
            completeContent: [],
            grade: null,
            published: null,
        }
    },
    watch: {
        entryNode () {
            this.completeContent = []
            this.setContent()
            this.tempNode = this.entryNode

            if (this.entryNode.entry !== null) {
                this.grade = this.entryNode.entry.grade
                this.published = this.entryNode.entry.published
            } else {
                this.grade = null
                this.published = true
            }
        },
    },
    created () {
        this.setContent()

        if (this.entryNode.entry) {
            this.grade = this.entryNode.entry.grade
            this.published = this.entryNode.entry.published
        }
    },
    methods: {
        setContent () {
            /* Loads in the data of an entry in the right order by matching
             * the different data-fields with the corresponding template-IDs. */
            let matchFound

            if (this.entryNode.entry !== null) {
                this.entryNode.entry.template.field_set.forEach((templateField) => {
                    matchFound = false

                    matchFound = this.entryNode.entry.content.some((content) => {
                        if (content.field === templateField.id) {
                            this.completeContent.push({
                                data: content.data,
                                id: content.field,
                                contentID: content.id,
                            })

                            return true
                        }

                        return false
                    })

                    if (!matchFound) {
                        this.completeContent.push({
                            data: null,
                            id: templateField.id,
                        })
                    }
                })
            }
        },
        commitGrade () {
            if (this.grade !== null) {
                this.tempNode.entry.grade = this.grade
                this.tempNode.entry.published = this.published

                if (this.published) {
                    entryAPI.grade(
                        this.entryNode.entry.id,
                        { grade: this.grade, published: 1 },
                        { customSuccessToast: 'Grade updated and published.' },
                    )
                        .then(() => { this.$emit('check-grade') })
                } else {
                    entryAPI.grade(
                        this.entryNode.entry.id,
                        { grade: this.grade, published: 0 },
                        { customSuccessToast: 'Grade updated but not published.' },
                    )
                        .then(() => { this.$emit('check-grade') })
                }
            }
        },
    },
}
</script>
