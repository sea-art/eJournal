<template>
    <div class="editor-container">
        <tiny-mce v-model="content" ref="mce" :init="config"/>
        <div v-html="content"/>
    </div>
</template>

<script>
// TODO Figure out why this gives a warning transferred with MIME type 2x

// TODO Deze kan global als tinymce niet meer direct gecalled wordt
import tinymce from 'tinymce/tinymce'
import 'tinymce/themes/modern/theme'

import 'tinymce/skins/lightgray/skin.min.css'
import TinyMCE from '@tinymce/tinymce-vue'

import 'tinymce/plugins/autoresize'

import 'tinymce/plugins/image'
import 'tinymce/plugins/imagetools'

import 'tinymce/plugins/link'
import 'tinymce/plugins/media'
import 'tinymce/plugins/preview'
import 'tinymce/plugins/print'

import 'tinymce/plugins/hr'

export default {
    name: 'TextEditor',
    data () {
        return {
            content: '',
            config: {
                menubar: true,
                branding: false,
                statusbar: false,

                /* Hides the menu untill selected pop up ontop */
                inline: false,

                menu: {
                    file: {title: 'File', items: 'newdocument preview print'},
                    edit: {title: 'Edit', items: 'undo redo | cut copy paste pastetext | selectall'},
                    insert: {title: 'Insert', items: 'link | template hr | media image'},
                    view: {title: 'View', items: 'visualaid'},
                    format: {title: 'Format', items: 'bold italic underline strikethrough superscript subscript | formats | removeformat'},
                    table: {title: 'Table', items: 'inserttable tableprops deletetable | cell row column'},
                    tools: {title: 'Tools', items: 'spellchecker code'}
                },
                content_css: ['//fonts.googleapis.com/css?family=Roboto+Condensed|Roboto:400,700'],
                // TODO Figure out why initial render ignores the font
                // font_formats: 'Robot Condensed = roboto condensed',
                // insert_button_items:
                plugins: ['autoresize', 'image', 'hr', 'link', 'media', 'preview', 'print'],
                image_title: true,

                // TODO Add more file support
                // Browser supposed to be deprecated, callback works nonetheless
                // file_browser_callback: this.handleFileBrowsing,
                // file_browser_callback_types: 'image'

                // TODO Kan weg als image upload handler werkt willen pdf en files toch niet in de editor
                file_picker_types: 'image',
                file_picker_callback: this.handleFilePicking,

                // automatic_uploads: true,
                // https://www.tiny.cloud/docs/advanced/php-upload-handler/
                // images_upload_url: TODO Create or not depending on the handler
                images_upload_handler: this.handleImageUpload
            }
        }
    },
    methods: {
        // https://www.tiny.cloud/docs/configure/file-image-upload
        handleImageUpload (blobInfo, success, failure) {
            console.log(blobInfo)
            console.log('Handle image upload')
        },
        handleFilePicking (cb, value, meta) {
            var input = document.createElement('input')
            input.setAttribute('type', 'file')
            input.setAttribute('accept', 'image/*')

            // Note: In modern browsers input[type="file"] is functional without
            // even adding it to the DOM, but that might not be the case in some older
            // or quirky browsers like IE, so you might want to add it to the DOM
            // just in case, and visually hide it.
            // TODO Remove input after click

            input.onchange = function () {
                // TODO Some file error handling
                var file = this.files[0]

                var reader = new FileReader()
                reader.onload = function () {
                    // Note: Now we need to register the blob in TinyMCEs image blob registry
                    var id = 'blobid' + (new Date()).getTime()
                    var blobCache = tinymce.activeEditor.editorUpload.blobCache
                    var base64 = reader.result.split(',')[1]
                    var blobInfo = blobCache.create(id, file, base64)
                    blobCache.add(blobInfo)

                    // call the callback and populate the Title field with the file name
                    cb(blobInfo.blobUri(), { title: file.name })
                }
                reader.readAsDataURL(file)
            }

            input.click()
        }
    },
    components: {
        'tiny-mce': TinyMCE
    }
}
</script>

<style lang="sass">
    .editor-container
        padding-right: 3px
</style>
