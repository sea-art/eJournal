<!--
    Loads a filled in template of an entry and the corresponding
    comments. The teacher tools will also be loaded if the user has the
    right permissions.
-->
<template>
    <div v-if="entryNode.entry !== null">
        <b-card class="entry-card no-hover entry-card-teacher" :class="$root.getBorderClass($route.params.cID)">
            <div v-if="$root.canGradeJournal()" class="grade-section shadow">
                <b-form-input class="theme-input" type="number" size="2" v-model="grade" placeholder="0" min=0></b-form-input>
                <b-form-checkbox v-model="published" value=true unchecked-value=false data-toggle="tooltip" title="Show grade to student">
                    Publish
                </b-form-checkbox>
                <b-button class="add-button" @click="commitGrade">
                    <icon name="save" scale="1"/>
                    Save
                </b-button>
            </div>
            <div v-else class="grade-section shadow">
                <span v-if="tempNode.entry.published">
                    {{ entryNode.entry.grade }}
                </span>
                <span v-else>
                    <icon name="hourglass-half"/>
                </span>
            </div>
            <h2 class="mb-2">{{entryNode.entry.template.name}}</h2>

            <div v-for="(field, i) in entryNode.entry.template.fields" class="entry-field" :key="field.eID">
                <div v-if="field.title != ''">
                    <b>{{ field.title }}</b>
                </div>
                <div v-if="field.type=='t'">
                    <span class="show-enters">{{ completeContent[i].data }}</span><br><br>
                </div>
                <div v-else-if="field.type=='i'">
                    <image-file-display
                        :fileName="completeContent[i].data"
                        :authorUID="$parent.journal.student.uID"
                    />
                </div>
                <div v-else-if="field.type=='f'">
                    <file-download-button
                        :fileName="completeContent[i].data"
                        :authorUID="$parent.journal.student.uID"
                    />
                </div>
                <div v-else-if="field.type=='v'">
                    <b-embed type="iframe"
                             aspect="16by9"
                             :src="completeContent[i].data"
                             allowfullscreen
                    ></b-embed><br>
                </div>
                <div v-else-if="field.type == 'p'">
                    <pdf-display
                        :fileName="completeContent[i].data"
                        :authorUID="$parent.journal.student.uID"
                    />
                </div>
                <div v-else-if="field.type == 'rt'" v-html="completeContent[i].data"/>
            </div>
        </b-card>

        <comment-card :eID="entryNode.entry.eID" :entryGradePublished="entryNode.entry.published"/>
    </div>
    <b-card v-else class="no-hover" :class="$root.getBorderClass($route.params.cID)">
        <h2 class="mb-2">{{entryNode.template.name}}</h2>
        <b>No submission for this student</b>
    </b-card>
</template>

<script>
import commentCard from '@/components/journal/CommentCard.vue'
import pdfDisplay from '@/components/assets/PdfDisplay.vue'
import fileDownloadButton from '@/components/assets/file_handling/FileDownloadButton.vue'
import imageFileDisplay from '@/components/assets/file_handling/ImageFileDisplay.vue'
import journalApi from '@/api/journal.js'
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['entryNode'],
    data () {
        return {
            tempNode: this.entryNode,
            completeContent: [],
            grade: null,
            published: null
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
        }
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
        commitGrade () {
            if (this.grade !== null) {
                this.tempNode.entry.grade = this.grade
                this.tempNode.entry.published = (this.published === 'true' || this.published === true)

                if (this.published === 'true' || this.published === true) {
                    journalApi.update_grade_entry(this.entryNode.entry.eID, this.grade, 1)
                        .then(_ => {
                            this.$toasted.success('Grade updated and published.')
                            this.$emit('check-grade')
                        })
                        .catch(error => { this.$toasted.error(error.response.data.description) })
                } else {
                    journalApi.update_grade_entry(this.entryNode.entry.eID,
                        this.grade, 0)
                        .then(_ => {
                            this.$toasted.success('Grade updated but not published.')
                            this.$emit('check-grade')
                        })
                        .catch(error => { this.$toasted.error(error.response.data.description) })
                }
            }
        }
    },
    components: {
        'comment-card': commentCard,
        'file-download-button': fileDownloadButton,
        'pdf-display': pdfDisplay,
        'image-file-display': imageFileDisplay,
        icon
    }
}
</script>
