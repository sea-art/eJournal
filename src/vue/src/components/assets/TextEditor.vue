<template>
    <div class="editor-container">
        <tiny-mce :id="'test1'" v-model="content" ref="mce" :init="config"/>
        <div v-html="content"/>
    </div>
</template>

<script>
import userAPI from '@/api/user.js'

// TODO Figure out why importing tinymce gives a warning transferred with MIME type 2x

import tinymce from 'tinymce/tinymce'
import 'tinymce/themes/modern/theme'

import 'tinymce/skins/lightgray/skin.min.css'
// TODO Custom component gaan maken
import TinyMCE from '@tinymce/tinymce-vue'

/* Only works with basic lists enabled. */
import 'tinymce/plugins/advlist'
import 'tinymce/plugins/autolink'
import 'tinymce/plugins/autoresize'
import 'tinymce/plugins/autosave'

/* Allows direct manipulation of the html aswell as easy export. */
import 'tinymce/plugins/code'

// TODO Make code sample work!
/* Allows for code block display, uses external prism for css and js. */
// import 'tinymce/plugins/codesample'

/* The colorpicker plugin adds an HSV color picker dialog to the editor.
When activated in conjunction with the textcolor plugin it adds a "custom color"
button to the text color toolbar dropdown. */
import 'tinymce/plugins/colorpicker'

import 'tinymce/plugins/fullscreen'

import 'tinymce/plugins/image'
import 'tinymce/plugins/imagetools'

import 'tinymce/plugins/link'
import 'tinymce/plugins/lists'

import 'tinymce/plugins/nonbreaking'
import 'tinymce/plugins/media'
import 'tinymce/plugins/preview'
import 'tinymce/plugins/print'

import 'tinymce/plugins/hr'
import 'tinymce/plugins/searchreplace'
import 'tinymce/plugins/spellchecker'

import 'tinymce/plugins/table'
import 'tinymce/plugins/textcolor'
import 'tinymce/plugins/textpattern'
/* Table of contents. */
import 'tinymce/plugins/toc'

import 'tinymce/plugins/wordcount'

// TODO implement
// https://moonwave99.github.io/TinyMCELatexPlugin/
// import 'tinymce/plugins/latex'

export default {
    name: 'TextEditor',
    props: {
        limitedColors: {
            type: Boolean,
            default: false
        },
        basic: {
            type: Boolean,
            default: false
        }
    },
    data () {
        return {
            content: '',
            config: {
                menubar: true,
                branding: false,
                statusbar: true,
                inline: false,
                image_title: true,

                autosave_ask_before_unload: true,
                autosave_interval: '10s',
                // autosave_restore_when_empty: true,
                // autosave_retention: '30m',

                /* Custom styling applied to the editor */
                content_css: ['//fonts.googleapis.com/css?family=Roboto+Condensed|Roboto:400,700'],

                file_picker_types: 'image',
                file_picker_callback: this.handleFilePicking,

                // automatic_uploads: true,
                images_upload_handler: this.handleImageUpload,

                plugins: [],

                toolbar1: '',
                setup: function (editor) {
                    console.log(editor)
                    editor.addButton('fullscreentoggle', {
                        icon: 'fullscreen',
                        onclick: function () {
                            editor.execCommand('mceFullScreen')
                            this.active(editor.plugins.fullscreen.isFullscreen())
                        },
                        /* If we ever start in fullscreen set correct state. */
                        onpostrender: function () {
                            var btn = this
                            editor.on('init', function () {
                                btn.active(editor.plugins.fullscreen.isFullscreen())
                            })
                        }
                    })
                    /* Set default font */
                    editor.on('init', function (e) {
                        editor.execCommand('fontName', false, 'roboto condensed')
                    })
                }
            },
            basicConfig: {
                toolbar1: 'bold italic underline alignleft aligncenter alignright alignjustify | forecolor backcolor restoredraft | formatselect | bullist numlist | image media table | removeformat fullscreentoggle',
                plugins: [
                    'autoresize textcolor image lists wordcount autolink autosave',
                    'table media fullscreen'
                ]
            },
            extensiveConfig: {
                toolbar1: 'bold italic underline alignleft aligncenter alignright alignjustify | forecolor backcolor | formatselect | bullist numlist | image media table | removeformat fullscreentoggle',
                plugins: [
                    'link media preview print hr lists advlist wordcount autolink autosave',
                    'autoresize code fullscreen image imagetools',
                    'textcolor searchreplace table toc latex'
                ]
            },
            extensiveConfigMenu: {
                menu: {
                    file: {title: 'File', items: 'newdocument restoredraft print'},
                    edit: {title: 'Edit', items: 'undo redo | cut copy paste | code | selectall searchreplace'},
                    insert: {title: 'Insert', items: 'image media link | hr | toc'},
                    view: {title: 'View', items: 'preview fullscreen'},
                    format: {title: 'Format', items: 'bold italic underline strikethrough superscript subscript | blockformats align | removeformat'},
                    table: {title: 'Table', items: 'inserttable tableprops deletetable | cell row column'}
                }
            }
        }
    },
    methods: {
        handleImageUpload (blobInfo, success, failure) {
            console.log(blobInfo)
            console.log('Handle image upload')

            let formData = new FormData()
            formData.append('file', blobInfo.blob())

            // TODO Create proper backend structure for serving files, this solution is dirty and should be treated as a proof of concept. */
            userAPI.updateImage(formData)
                .then(response => {
                    let fullFilePath = response.data.result.location
                    let staticPath = fullFilePath.match(/static\/.*(\..*)$/)[0]
                    success('../../../' + staticPath)
                })
                .catch(_ => { this.$toasted.error('Something went wrong while uploading your requested image.') })
        },
        handleFilePicking (cb, value, meta) {
            /* Client side allows for handling of files more than image types, which a plugin currently handles. */
            console.log('filePicking')
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
                    var blobInfo = blobCache.create(id, file, base64, file.name.replace(/\.[^/.]+$/, ''))
                    blobCache.add(blobInfo)

                    // call the callback and populate the Title field with the file name
                    cb(blobInfo.blobUri(), { title: file.name })
                }
                reader.readAsDataURL(file)
            }

            input.click()
        },
        setCustomColors () {
            /* Enables some basic colors too chose from, inline with the websites theme colors. */
            this.config.textcolor_cols = 4
            this.config.textcolor_rows = 1
            this.config.textcolor_map = [
                '252C39', 'Theme dark blue',
                '007E33', 'Theme positive selected',
                'FF8800', 'Theme change selected',
                'CC0000', 'Theme negative selected'
            ]
        },
        setBasicConfig () {
            this.config.menubar = false
            this.config.toolbar1 = this.basicConfig.toolbar1
            this.config.plugins = this.basicConfig.plugins
        },
        setExtensiveConfig () {
            this.config.menubar = true
            this.config.toolbar1 = this.extensiveConfig.toolbar1
            this.config.plugins = this.extensiveConfig.plugins
            this.config.menu = this.extensiveConfigMenu.menu
        },
        enableTabs () {
            /* Three space tabs, breaks tabbing through table entries (choice) */
            this.config.plugins.push('nonbreaking')
            this.config.nonbreaking_force_tab = true
        },
        enableBrowserSpellchecker () {
            this.config.plugins.push('spellchecker')
            this.config.browser_spellcheck = true
        },
        enableMarkdownPatterns () {
            this.config.plugins.push('textpattern')
            this.config.textpattern_patterns = [
                {start: '*', end: '*', format: 'italic'},
                {start: '**', end: '**', format: 'bold'},
                {start: '#', format: 'h1'},
                {start: '##', format: 'h2'},
                {start: '###', format: 'h3'},
                {start: '####', format: 'h4'},
                {start: '#####', format: 'h5'},
                {start: '######', format: 'h6'},
                {start: '1. ', cmd: 'InsertOrderedList'},
                {start: '* ', cmd: 'InsertUnorderedList'},
                {start: '- ', cmd: 'InsertUnorderedList'}
            ]
        }
    },
    created () {
        if (this.basic) {
            this.setBasicConfig()
        } else {
            this.setExtensiveConfig()
        }

        if (this.limitedColors) {
            this.setCustomColors()
        } else {
            this.config.plugins.push('colorpicker')
        }

        this.enableTabs()
        this.enableBrowserSpellchecker()
        this.enableMarkdownPatterns()
    },
    components: {
        'tiny-mce': TinyMCE
    }
}
</script>

<style lang="sass">
.editor-container
    padding: 0px 3px

.mce-fullscreen
    padding-top: 70px
</style>
