<!--
    Loads in an entry for a student, which was previously filled in
    by the student using an Add-Node or an empty Deadline-Entry-Node.
    It will also show the grade once it's published by responsible user
    and give a possibility to edit an entry if it still has the
    needed privileges.
 -->
<template>
    <div>
        <!-- Edit mode. -->
        <b-card v-if="saveEditMode == 'Save'" class="entry-card no-hover" :class="$root.getBorderClass(cID)">
            <div class="grade-section shadow">
                <span v-if="entryNode.entry.published">
                    {{ entryNode.entry.grade }}
                </span>
                <span v-else>
                    <icon name="hourglass-half"/>
                </span>
            </div>
            <h2 class="mb-2">{{entryNode.entry.template.name}}</h2>
            <!--
                Shows every field description and
                a corresponding form.
            -->
            <div v-for="(field, i) in entryNode.entry.template.fields" :key="field.eID">
                <div v-if="field.title">
                    <b>{{ field.title }}</b>
                </div>

                <div v-if="field.type=='t'">
                    <b-textarea class="theme-input" v-model="completeContent[i].data"></b-textarea><br>
                </div>
                <div v-else-if="field.type=='i'">
                    <b-form-file v-model="completeContent[i].data" :state="Boolean(completeContent[i].data)" placeholder="Choose a file..."></b-form-file><br>
                </div>
                <div v-else-if="field.type=='f'">
                    <b-form-file v-model="completeContent[i].data" :state="Boolean(completeContent[i].data)" placeholder="Choose a file..."></b-form-file><br>
                </div>
                <!--
                    We use @input here instead of v-model so we can format the data differently (and make use of existing checks),
                    and because it is not needed to reload the data into the input field upon editing
                    (since it is an entire URL, replacement is preferable over editing).
                -->
                <div v-else-if="field.type=='v'">
                    <b-input class="theme-input" @input="completeContent[i].data = youtubeEmbedFromURL($event)"></b-input><br>
                </div>
            </div>
            <b-alert :show="dismissCountDown" dismissible variant="secondary"
                @dismissed="dismissCountDown=0">
                Some fields are empty or incorrectly formatted.
            </b-alert>
            <b-button class="add-button float-right" @click="saveEdit">
                <icon name="save"/>
                Save
            </b-button>
            <b-button class="delete-button" @click="cancel">
                <icon name="ban"/>
                Cancel
            </b-button>
        </b-card>
        <!-- Overview mode. -->
        <b-card v-else class="entry-card no-hover" :class="$root.getBorderClass(cID)">
            <div class="grade-section shadow">
                <span v-if="entryNode.entry.published">
                    {{ entryNode.entry.grade }}
                </span>
                <span v-else>
                    <icon name="hourglass-half"/>
                </span>
            </div>
            <h2 class="mb-2">{{entryNode.entry.template.name}}</h2>
            <!--
                Gives a view of every templatefield and
                if possible the already filled in entry.
            -->
            <div v-for="(field, i) in entryNode.entry.template.fields" :key="field.eID">
                <div v-if="field.title">
                    <b>{{ field.title }}</b>
                </div>
                <div v-if="field.type=='t'">
                    <span class="show-enters">{{ completeContent[i].data }}</span><br>
                </div>
                <div v-else-if="field.type=='i'">
                    {{ completeContent[i].data }}<br>
                </div>
                <div v-else-if="field.type=='f'">
                    {{ completeContent[i].data }}<br>
                </div>
                <div v-else-if="field.type=='v'">
                    <b-embed type="iframe"
                             aspect="16by9"
                             :src="completeContent[i].data"
                             allowfullscreen
                    ></b-embed><br>
                </div>
            </div>
            <b-button v-if="entryNode.entry.editable" class="change-button float-right" @click="saveEdit">
                <icon name="edit"/>
                Edit
            </b-button>
        </b-card>

        <comment-card :eID="entryNode.entry.eID"/>
    </div>
</template>

<script>
import commentCard from '@/components/journal/CommentCard.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['entryNode', 'cID'],
    data () {
        return {
            saveEditMode: 'Edit',
            tempNode: this.entryNode,
            matchEntry: 0,
            completeContent: [],

            dismissSecs: 3,
            dismissCountDown: 0,
            showDismissibleAlert: false
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
                if (this.checkFilled()) {
                    this.saveEditMode = 'Edit'
                    this.tempNode.entry.content = this.completeContent
                    this.$emit('edit-node', this.tempNode)
                } else {
                    this.dismissCountDown = this.dismissSecs
                }
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
        },
        checkFilled: function () {
            for (var content of this.completeContent) {
                if (!content.data) {
                    return false
                }
            }

            return true
        },
        // from https://stackoverflow.com/a/9102270
        youtubeEmbedFromURL (url) {
            var regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/
            var match = url.match(regExp)
            if (match && match[2].length === 11) {
                return 'https://www.youtube.com/embed/' + match[2] + '?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media'
            } else {
                return null
            }
        }
    },
    components: {
        'comment-card': commentCard,
        'icon': icon
    }
}
</script>
