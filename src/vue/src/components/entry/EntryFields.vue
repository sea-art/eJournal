<template>
    <div v-if="!displayMode">
        <div
            v-for="(field, i) in template.field_set.sort((a, b) => a.location - b.location)"
            :key="`node ${nodeID}-field-${field.id}`"
            class="multi-form"
        >
            <h2
                v-if="field.title"
                :class="{ 'required': field.required }"
                class="field-heading"
            >
                {{ field.title }}
            </h2>
            <sandboxed-iframe
                v-if="field.description"
                :content="field.description"
            />

            <b-input
                v-if="field.type == 't'"
                v-model="completeContent[i].data"
                class="theme-input"
                rows="1"
            />
            <flat-pickr
                v-if="field.type == 'd'"
                v-model="completeContent[i].data"
                class="theme-input full-width"
            />

            <file-upload-input
                v-else-if="field.type == 'i'"
                :placeholder="completeContent[i].data"
                :acceptedFiletype="'image/*'"
                :maxSizeBytes="$root.maxFileSizeBytes"
                :autoUpload="true"
                :aID="$route.params.aID"
                :contentID="completeContent[i].contentID"
                @fileUploadSuccess="completeContent[i].data = $event"
            />
            <file-upload-input
                v-else-if="field.type == 'f'"
                :placeholder="completeContent[i].data"
                :acceptedFiletype="'*/*'"
                :maxSizeBytes="$root.maxFileSizeBytes"
                :autoUpload="true"
                :aID="$route.params.aID"
                :contentID="completeContent[i].contentID"
                @fileUploadSuccess="completeContent[i].data = $event"
            />
            <b-input
                v-else-if="field.type == 'v'"
                :placeholder="completeContent[i].data ? completeContent[i].data : 'Enter YouTube URL...'"
                class="theme-input"
                @input="completeContent[i].data = youtubeEmbedFromURL($event)"
            />
            <file-upload-input
                v-else-if="field.type == 'p'"
                :placeholder="completeContent[i].data"
                :acceptedFiletype="'application/pdf'"
                :maxSizeBytes="$root.maxFileSizeBytes"
                :autoUpload="true"
                :aID="$route.params.aID"
                :contentID="completeContent[i].contentID"
                @fileUploadSuccess="completeContent[i].data = $event"
            />
            <text-editor
                v-else-if="field.type == 'rt'"
                :id="'rich-text-editor-field-' + i"
                v-model="completeContent[i].data"
            />
            <url-input
                v-else-if="field.type == 'u'"
                :placeholder="completeContent[i].data"
                @correctUrlInput="completeContent[i].data = $event"
            />
            <b-form-select
                v-else-if="field.type == 's'"
                v-model="completeContent[i].data"
                :options="parseSelectionOptions(field.options)"
            />
        </div>
    </div>
    <!-- Display section -->
    <div v-else>
        <div
            v-for="field in fieldsToDisplay.sort((a, b) => a.location - b.location)"
            :key="`node-${nodeID}-field-${field.id}`"
            class="multi-form"
        >
            <h2
                v-if="field.title"
                :class="{ 'required': field.required }"
                class="field-heading"
            >
                {{ field.title }}
            </h2>
            <span
                v-if="field.type == 't'"
                class="show-enters"
            >{{ completeContent[field.location].data }}</span>
            <span
                v-if="field.type == 'd'"
                class="show-enters"
            >{{ $root.beautifyDate(completeContent[field.location].data) }}</span>
            <image-file-display
                v-else-if="field.type == 'i'"
                :id="'image-display-field-' + field.location"
                :fileName="completeContent[field.location].data"
                :authorUID="authorUID"
                :entryID="entryID"
                :nodeID="nodeID"
                :contentID="completeContent[field.location].contentID"
            />
            <file-download-button
                v-else-if="field.type == 'f'"
                :fileName="completeContent[field.location].data"
                :authorUID="authorUID"
                :entryID="entryID"
                :nodeID="nodeID"
                :contentID="completeContent[field.location].contentID"
            />
            <b-embed
                v-else-if="field.type == 'v'"
                :src="completeContent[field.location].data"
                type="iframe"
                aspect="16by9"
                allowfullscreen
            />
            <pdf-display
                v-else-if="field.type == 'p'"
                :fileName="completeContent[field.location].data"
                :authorUID="authorUID"
                :entryID="entryID"
                :nodeID="nodeID"
                :contentID="completeContent[field.location].contentID"
            />
            <sandboxed-iframe
                v-else-if="field.type == 'rt'"
                :content="completeContent[field.location].data"
            />
            <a
                v-else-if="field.type == 'u'"
                :href="completeContent[field.location].data"
            >{{ completeContent[field.location].data }}</a>
            <span v-else-if="field.type == 's'">{{ completeContent[field.location].data }}</span>
        </div>
    </div>
</template>

<script>
import fileUploadInput from '@/components/assets/file_handling/FileUploadInput.vue'
import textEditor from '@/components/assets/TextEditor.vue'
import urlInput from '@/components/assets/UrlInput.vue'
import fileDownloadButton from '@/components/assets/file_handling/FileDownloadButton.vue'
import imageFileDisplay from '@/components/assets/file_handling/ImageFileDisplay.vue'
import pdfDisplay from '@/components/assets/PdfDisplay.vue'
import sandboxedIframe from '@/components/assets/SandboxedIframe.vue'

export default {
    components: {
        fileUploadInput,
        textEditor,
        urlInput,
        pdfDisplay,
        fileDownloadButton,
        imageFileDisplay,
        sandboxedIframe,
    },
    props: {
        template: {
            required: true,
        },
        completeContent: {
            default: false,
        },
        displayMode: {
            type: Boolean,
            required: true,
        },
        nodeID: {
            required: true,
        },
        authorUID: {
            default: null,
            required: false,
        },
        entryID: {
            default: '-1',
        },
    },
    computed: {
        fieldsToDisplay () {
            return this.template.field_set.filter((field, i) => (field.required || this.completeContent[i].data))
        },
    },
    created () {
        this.template.field_set.sort((a, b) => a.location - b.location)
    },
    methods: {
        // from https://stackoverflow.com/a/9102270
        youtubeEmbedFromURL (url) {
            const regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/
            const match = url.match(regExp)
            if (match && match[2].length === 11) {
                return `https://www.youtube.com/embed/${match[2]}?rel=0&amp;showinfo=0`
            } else {
                return null
            }
        },
        parseSelectionOptions (fieldOptions) {
            if (!fieldOptions) {
                return [{ value: null, text: 'Please select an option...' }]
            }
            const options = JSON.parse(fieldOptions).filter(e => e).map(x => Object({ value: x, text: x }))
            options.unshift({ value: null, text: 'Please select an option...' })
            return options
        },
        checkChanges () {
            for (let i = 0; i < this.completeContent.length; i++) {
                if (this.completeContent[i].data !== null && this.completeContent[i].data !== '') {
                    return true
                }
            }
            return false
        },
    },
}
</script>
