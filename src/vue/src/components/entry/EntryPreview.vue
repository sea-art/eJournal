<!--
    Loads a preview of an Entry-Template and returns the filled in data to
    the parent once it's saved.
-->
<template>
    <div>
        <b-card class="no-hover" :class="$root.getBorderClass(cID)">
            <h2 class="mb-2">{{ template.name }}</h2>
            <div v-for="(field, i) in template.field_set" :key="field.eID">
                <div v-if="field.title != ''">
                    <b>{{ field.title }}</b>
                </div>

                <div v-if="field.type=='t'">
                    <b-textarea class="theme-input" v-model="completeContent[i].data"></b-textarea><br>
                </div>
                <div v-else-if="field.type=='i'">
                    <file-upload-input
                        :acceptedFiletype="'image/*'"
                        :maxSizeBytes="$root.maxFileSizeBytes"
                        :autoUpload="true"
                        @fileUploadSuccess="completeContent[i].data = $event"
                        :aID="$route.params.aID"
                    />
                </div>
                <div v-else-if="field.type=='f'">
                    <file-upload-input
                        :acceptedFiletype="'*/*'"
                        :maxSizeBytes="$root.maxFileSizeBytes"
                        :autoUpload="true"
                        @fileUploadSuccess="completeContent[i].data = $event"
                        :aID="$route.params.aID"
                    />
                </div>
                <div v-else-if="field.type=='v'">
                    <b-input class="theme-input" @input="completeContent[i].data = youtubeEmbedFromURL($event)" placeholder="Enter YouTube URL..."></b-input><br>
                </div>
                <div v-else-if="field.type == 'p'">
                    <file-upload-input
                        :acceptedFiletype="'application/pdf'"
                        :maxSizeBytes="$root.maxFileSizeBytes"
                        :autoUpload="true"
                        @fileUploadSuccess="completeContent[i].data = $event"
                        :aID="$route.params.aID"
                    />
                </div>
                <div v-else-if="field.type == 'rt'">
                    <text-editor
                        :id="'rich-text-editor-' + i"
                        @content-update="completeContent[i].data = $event"
                    />
                </div>
                <div v-else-if="field.type == 'u'">
                    <url-input @correctUrlInput="completeContent[i].data = $event"></url-input>
                </div>
            </div>

            <b-alert :show="dismissCountDown" dismissible variant="secondary"
                @dismissed="dismissCountDown=0">
                Some fields are empty or incorrectly formatted.
            </b-alert>
            <b-button class="add-button float-right mt-2" @click="save">
                <icon name="paper-plane"/>
                Post Entry
            </b-button>
        </b-card>
    </div>
</template>

<script>
import icon from 'vue-awesome/components/Icon'
import fileUploadInput from '@/components/assets/file_handling/FileUploadInput.vue'
import textEditor from '@/components/assets/TextEditor.vue'
import urlInput from '@/components/assets/UrlInput.vue'

export default {
    props: ['template', 'cID'],
    data () {
        return {
            completeContent: [],
            dismissSecs: 3,
            dismissCountDown: 0,
            showDismissibleAlert: false
        }
    },
    watch: {
        template: function () {
            this.completeContent = []
            this.setContent()
        }
    },
    created () {
        this.setContent()
    },
    methods: {
        setContent: function () {
            for (var field of this.template.field_set) {
                this.completeContent.push({
                    data: null,
                    id: field.id
                })
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
        save: function () {
            if (this.checkFilled()) {
                this.$emit('content-template', this.completeContent)
            } else {
                this.dismissCountDown = this.dismissSecs
            }
        },
        // from https://stackoverflow.com/a/9102270
        youtubeEmbedFromURL (url) {
            var regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/
            var match = url.match(regExp)
            if (match && match[2].length === 11) {
                return 'https://www.youtube.com/embed/' + match[2] + '?rel=0&amp;showinfo=0'
            } else {
                return null
            }
        }
    },
    components: {
        icon,
        'file-upload-input': fileUploadInput,
        'text-editor': textEditor,
        'url-input': urlInput
    }
}
</script>
