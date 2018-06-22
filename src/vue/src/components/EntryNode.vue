<!-- Example of a simple template. -->
<template>
    <div class="entry-template">
        hoi {{dataComments}}
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                <div v-if="saveEditMode == 'Save'">
                    <!-- Edit mode. -->
                    <b-card class="card main-card no-hover" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <h2>{{entryNode.entry.template.name}}</h2>
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12" class="right-content">
                                <div v-if="entryNode.entry.grade != 0">
                                    {{ entryNode.entry.grade }}
                                </div>
                                <div v-else>
                                    To be grated
                                </div>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                                <!-- Shows every field description and
                                    a corresponding form.
                                -->
                                <div v-for="(field, i) in entryNode.entry.template.fields" :key="field.eID">
                                    <div v-if="field.title != ''">
                                        <h4>{{ field.title }}</h4>
                                    </div>

                                    <div v-if="field.type=='t'">
                                        <b-textarea v-model="completeContent[i].data"></b-textarea><br><br>
                                    </div>
                                    <div v-else-if="field.type=='i'">
                                    </div>
                                    <div v-else-if="field.type=='f'">
                                    </div>
                                </div>
                                <b-button @click="saveEdit">{{ saveEditMode }} </b-button>
                                <b-button @click="cancel">Cancel</b-button>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
                <div v-else>
                    <!-- Overview mode. -->
                    <b-card class="card main-card no-hover" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <h2>{{entryNode.entry.template.name}}</h2>
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12" class="right-content">
                                <div v-if="entryNode.entry.grade != 0">
                                    {{ entryNode.entry.grade }}
                                </div>
                                <div v-else>
                                    To be graded
                                </div>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                                <!-- Gives a view of every templatefield and
                                    if possible the already filled in entry.
                                -->
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
                                <b-button @click="saveEdit">{{ saveEditMode }} </b-button>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
            </b-col>
        </b-row>

        <comment-card @new-comments="addComment" :comments="comments" :person="'Henk'" :eID="entryNode.entry.eID"/>
    </div>
</template>

<script>
import commentCard from '@/components/CommentCard.vue'
import entryApi from '@/api/entry.js'

export default {
    props: ['entryNode'],
    data () {
        return {
            saveEditMode: 'Edit',
            tempNode: this.entryNode,
            matchEntry: 0,
            completeContent: [],
            dataComments: [],
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
        }
    },
    created () {
        this.loadComments()
        this.setContent()
    },
    methods: {
        saveEdit: function () {
            if (this.saveEditMode === 'Save') {
                this.saveEditMode = 'Edit'
                this.tempNode.entry.content = this.completeContent
                this.$emit('edit-node', this.tempNode)
            } else {
                this.saveEditMode = 'Save'
                this.completeContent = []
                this.setContent()
            }
        },
        cancel: function () {
            this.saveEditMode = 'Edit'
            this.completeContent = []
            this.setContent()
        },
        setContent: function () {
            var checkFound = false
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
        },
        loadComments: function () {
            entryApi.get_entrycomments(this.entryNode.entry.eID).then(response => { this.dataComments = response })
        },
        addComment: function (newComment) {
            this.comments.push(newComment)
            entryApi.create_entrycomments(this.entryNode.entry.eID, 'Rein', newComment)
        }
    },
    components: {
        'comment-card': commentCard
    }
}

</script>
