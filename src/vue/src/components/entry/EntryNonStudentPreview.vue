<!--
    Loads a filled in template of an entry and the corresponding
    comments. The teacher tools will also be loaded if the user has the
    right permissions.
-->
<template>
    <div v-if="entryNode.entry !== null">
        <b-card class="main-card no-hover entry-card" :class="$root.getBorderClass($route.params.cID)">
            <div class="template-name">
                <h2>{{entryNode.entry.template.name}}</h2>
            </div>
            <div v-if="$root.canGradeJournal()" class="grade-section-teacher shadow no-hover">
                <b-form-input type="number" size="2" v-model="grade" placeholder="0" min=0></b-form-input>
                <b-form-checkbox v-model="status" value=true unchecked-value=false data-toggle="tooltip" title="Show grade to student">
                    Publish
                </b-form-checkbox>
                <b-button class="add-button" @click="commitGrade">
                    <icon name="save" scale="1"></icon>
                    Save
                </b-button>
            </div>
            <div v-else class="grade-section shadow">
                <span v-if="tempNode.entry.published">
                    {{ entryNode.entry.grade }}
                </span>
                <span v-else>
                    <icon name="hourglass-half"></icon>
                </span>
            </div>

            <div v-for="(field, i) in entryNode.entry.template.fields" class="entry-field" :key="field.eID">
                <div v-if="field.title != ''">
                    <b>{{ field.title }}</b>
                </div>
                <div v-if="field.type=='t'">
                    <span class="show-enters">{{ completeContent[i].data }}</span><br><br>
                </div>
                <div v-else-if="field.type=='i'">
                </div>
                <div v-else-if="field.type=='f'">
                </div>
            </div>
        </b-card>

        <comment-card :eID="entryNode.entry.eID"/>
    </div>
    <b-card v-else class="no-hover">
        <b>No submission for this student</b>
    </b-card>
</template>

<script>
import commentCard from '@/components/journal/CommentCard.vue'
import journalApi from '@/api/journal.js'
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['entryNode'],
    data () {
        return {
            tempNode: this.entryNode,
            completeContent: [],
            grade: this.entryNode.entry.grade,
            status: this.entryNode.entry.published
        }
    },
    watch: {
        entryNode: function () {
            this.completeContent = []
            this.setContent()
            this.tempNode = this.entryNode

            if (this.entryNode.entry !== null) {
                this.grade = this.entryNode.entry.grade
                this.status = this.entryNode.entry.published
            } else {
                this.grade = null
                this.status = true
            }
        }
    },
    created () {
        this.setContent()
    },
    methods: {
        setContent: function () {
            /* Loads in the data of an entry in the right order by matching
             * the different data-fields with the corresponding template-IDs. */
            var checkFound = false

            if (this.entryNode.entry !== null) {
                for (var templateField of this.entryNode.entry.template.fields) {
                    checkFound = false

                    for (var content of this.entryNode.entry.content) {
                        if (content.tag === templateField.tag) {
                            this.completeContent.push({
                                data: content.data,
                                tag: content.tag
                            })

                            checkFound = true
                            break
                        }
                    }

                    if (!checkFound) {
                        this.completeContent.push({
                            data: null,
                            tag: templateField.tag
                        })
                    }
                }
            }
        },
        commitGrade: function () {
            if (this.grade !== null) {
                this.tempNode.entry.grade = this.grade
                this.tempNode.entry.published = (this.status === 'true' || this.status === true)

                if (this.status === 'true' || this.status === true) {
                    journalApi.update_grade_entry(this.entryNode.entry.eID, this.grade, 1)
                        .then(_ => {
                            this.$toasted.success('Grade updated and published.')
                            this.$emit('check-grade')
                        })
                        .catch(_ => {
                            this.$toasted.error('Something went wrong with updating the grade.')
                        })
                } else {
                    journalApi.update_grade_entry(this.entryNode.entry.eID,
                        this.grade, 0)
                        .then(_ => {
                            this.$toasted.success('Grade updated but not published.')
                            this.$emit('check-grade')
                        })
                        .catch(_ => {
                            this.$toasted.error('Something went wrong with updating the grade.')
                        })
                }
            }
        }
    },
    components: {
        'comment-card': commentCard,
        'icon': icon
    }
}
</script>
