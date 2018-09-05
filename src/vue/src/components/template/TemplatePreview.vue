<!-- Loads a preview of a template. -->
<template>
    <b-card class="no-hover">
        <div v-for="(field, i) in template.field_set" :key="field.eID" class="multi-form">
            <span v-if="field.title">{{ field.title }}</span>

            <b-textarea
                v-if="field.type == 't'"
                class="theme-input"
            />
            <file-upload-input
                v-else-if="field.type == 'i'"
                :acceptedFiletype="'image/*'"
                :maxSizeBytes="$root.maxFileSizeBytes"
                :autoUpload="false"
                :aID="$route.params.aID"
            />
            <file-upload-input
                v-else-if="field.type == 'f'"
                :acceptedFiletype="'*/*'"
                :maxSizeBytes="$root.maxFileSizeBytes"
                :autoUpload="false"
                :aID="$route.params.aID"
            />
            <b-input v-else-if="field.type=='v'"
                class="theme-input"
                placeholder="Enter YouTube URL..."
            />
            <file-upload-input v-else-if="field.type == 'p'"
                :acceptedFiletype="'application/pdf'"
                :maxSizeBytes="$root.maxFileSizeBytes"
                :autoUpload="false"
                :aID="$route.params.aID"
            />
            <text-editor v-else-if="field.type == 'rt'"
                :id="'rich-text-editor-preview-field-' + i"
            />
            <url-input
                v-else-if="field.type == 'u'"
            />
        </div>
    </b-card>
</template>

<script>
import fileUploadInput from '@/components/assets/file_handling/FileUploadInput.vue'
import pdfDisplay from '@/components/assets/PdfDisplay.vue'
import textEditor from '@/components/assets/TextEditor.vue'
import icon from 'vue-awesome/components/Icon'
import urlInput from '@/components/assets/UrlInput.vue'

export default {
    props: ['template'],
    components: {
        'pdf-display': pdfDisplay,
        'file-upload-input': fileUploadInput,
        'text-editor': textEditor,
        'url-input': urlInput,
        icon
    }
}
</script>
