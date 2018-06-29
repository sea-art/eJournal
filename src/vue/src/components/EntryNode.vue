<!--
    Loads in an entry for a student, which was previously filled in
    by the student using an Add-Node or an empty Deadline-Entry-Node.
    It will also show the grade once it's published by responsible user
    and give a possibility to edit an entry if it still has the
    needed privileges.
 -->
<template>
    <div class="entry-template">
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
                                <div v-if="entryNode.entry.published">
                                    Points: {{ entryNode.entry.grade }}
                                </div>
                                <div v-else>
                                    To be graded
                                </div>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                                <!--
                                    Shows every field description and
                                    a corresponding form.
                                -->
                                <div v-for="(field, i) in entryNode.entry.template.fields" :key="field.eID">
                                    <div v-if="field.title != ''">
                                        <b>{{ field.title }}</b>
                                    </div>

                                    <div v-if="field.type=='t'">
                                        <b-textarea v-model="completeContent[i].data"></b-textarea><br><br>
                                    </div>
                                    <div v-else-if="field.type=='i'">
                                        <b-form-file v-model="completeContent[i].data" :state="Boolean(completeContent[i].data)" placeholder="Choose a file..."></b-form-file><br><br>
                                    </div>
                                    <div v-else-if="field.type=='f'">
                                        <b-form-file v-model="completeContent[i].data" :state="Boolean(completeContent[i].data)" placeholder="Choose a file..."></b-form-file><br><br>
                                    </div>
                                </div>
                                <b-button class="add-button" @click="saveEdit">{{ saveEditMode }} </b-button>
                                <b-button class="change-button" @click="cancel">Cancel</b-button>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
                <div v-else>
                    <!-- Overview mode. -->
                    <b-card class="card main-card no-hover" :class="this.$root.getBorderClass($route.params.cID)">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <h2>{{entryNode.entry.template.name}}</h2>
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12" class="right-content">
                                <div v-if="entryNode.entry.published">
                                    Points: {{ entryNode.entry.grade }}
                                </div>
                                <div v-else>
                                    <div v-if="entryNode.entry.editable">
                                        To be graded
                                    </div>
                                    <div v-else>
                                        Grade is not visible
                                    </div>
                                </div>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                                <!--
                                    Gives a view of every templatefield and
                                    if possible the already filled in entry.
                                -->
                                <div v-for="(field, i) in entryNode.entry.template.fields" :key="field.eID">
                                    <div v-if="field.title != ''">
                                        <b>{{ field.title }}</b>
                                    </div>
                                    <div v-if="field.type=='t'">
                                        <span class="showEnters">{{ completeContent[i].data }}</span><br><br>
                                    </div>
                                    <div v-else-if="field.type=='i'">
                                        {{ completeContent[i].data }}<br><br>
                                    </div>
                                    <div v-else-if="field.type=='f'">
                                        {{ completeContent[i].data }}<br><br>
                                    </div>
                                </div>
                                <b-button v-if="entryNode.entry.editable" @click="saveEdit">{{ saveEditMode }} </b-button>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
            </b-col>
        </b-row>

        <comment-card :eID="entryNode.entry.eID"/>
    </div>
</template>

<script>
import commentCard from '@/components/CommentCard.vue'

export default {
    props: ['entryNode'],
    data () {
        return {
            saveEditMode: 'Edit',
            tempNode: this.entryNode,
            matchEntry: 0,
            completeContent: []
        }
    },
    watch: {
        entryNode: function () {
            this.completeContent = []
            this.tempNode = this.entryNode
            this.setContent()
        }
    },
    created () {
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
            /* Loads in the data of an entry in the right order by matching
             * the different data-fields with the corresponding template-IDs. */
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
        }
    },
    components: {
        'comment-card': commentCard
    }
}

</script>
