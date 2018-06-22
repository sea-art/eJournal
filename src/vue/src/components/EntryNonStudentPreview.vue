<!-- Loads a preview of a template. -->
<template>
    <div v-if="entryNode.entry !== null">
        <b-card class="card main-card no-hover" :class="'dark-border'">
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
                            <h4>{{ field.title }}</h4>
                        </div>
                        <div v-if="field.type=='t'">
                            {{ completeContent[i].data }}<br><br>
                        </div>
                        <div v-else-if="field.type=='i'">
                        </div>
                        <div v-else-if="field.type=='f'">
                        </div>
                    </div>
                    <br>
                    Fill in the grade:<br>
                    <b-form-input type="number" v-model="grade" placeholder="Grade"></b-form-input>
                    <b-form-checkbox v-model="status" value=1 unchecked-value=0>
                        Show grade to student
                    </b-form-checkbox><br>
                    <b-button @click="commitGrade">Grade</b-button>
                </b-col>
            </b-row>
        </b-card>

        <comment-card @new-comments="addComment" :comments="comments" :person="'Henk'" :eID="entryNode.entry.eID"/>
    </div>
</template>

<script>
import commentCard from '@/components/CommentCard.vue'
import journalApi from '@/api/journal.js'

export default {
    props: ['entryNode'],
    data () {
        return {
            tempNode: this.entryNode,
            completeContent: [],
            grade: null,
            status: 1,

            comments: [{
                message: 'Hoi het is super slecht, ga je schamen!',
                person: 'Peter'
            }, {
                message: 'Hoi het is super goed!',
                person: 'Ptheven'
            }]
        }
    },
    watch: {
        entryNode: function () {
            this.completeContent = []
            this.setContent()

            if (this.entryNode.entry !== null) {
                this.grade = this.entryNode.entry.grade
                this.status = this.entryNode.entry.published
            } else {
                this.grade = null
                this.status = 1
            }
        }
    },
    created () {
        this.setContent()
    },
    methods: {
        setContent: function () {
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
        addComment: function (newComments) {
            this.comments = newComments
        },
        commitGrade: function () {
            if (this.grade !== null) {
                journalApi.update_grade_entry(this.entryNode.entry.eID, this.grade, this.status)
                confirm('Oh yeah! grade updated')
            }
        }
    },
    components: {
        'comment-card': commentCard
    }
}
</script>
