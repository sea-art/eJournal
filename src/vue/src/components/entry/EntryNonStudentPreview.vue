<!--
    Loads a filled in template of an entry and the corresponding
    comments. The teacher tools will also be loaded if the user has the
    right permissions.
-->
<template>
    <div v-if="entryNode.entry !== null">
        <b-card class="card main-card no-hover" :class="$root.getBorderClass($route.params.cID)">
            <b-row>
                <b-col id="main-card-left-column" cols="9" lg-cols="12">
                    <h2>{{entryNode.entry.template.name}}</h2>
                </b-col>
                <b-col id="main-card-right-column" cols="3" lg-cols="12" class="right-content">
                </b-col>
            </b-row>
            <b-row>
                <b-col id="main-card-left-column" cols="12" lg-cols="12">
                    <div v-for="(field, i) in entryNode.entry.template.fields" :key="field.eID">
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

                    <div v-if="$root.canGradeJournal()">
                        <br>
                        Fill in the grade:<br>
                        <b-form-input class="theme-input" type="number" v-model="grade" placeholder="Grade" min=0></b-form-input>
                        <b-form-checkbox v-model="status" value=true unchecked-value=false>
                            Show grade to student
                        </b-form-checkbox><br>
                        <b-button @click="commitGrade">Grade</b-button>
                    </div>
                    <div v-else>
                        <div v-if="tempNode.entry.published">
                            Points: {{ entryNode.entry.grade }}
                        </div>
                        <div v-else>
                            To be graded
                        </div>
                    </div>
                </b-col>
            </b-row>
        </b-card>

        <comment-card :eID="entryNode.entry.eID"/>
    </div>
</template>

<script>
import commentCard from '@/components/journal/CommentCard.vue'
import journalApi from '@/api/journal.js'

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
        'comment-card': commentCard
    }
}
</script>
