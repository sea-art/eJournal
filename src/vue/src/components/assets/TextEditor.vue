<!-- Custom wrapper for tinymce editor -->
<!-- If more events are desired, here is an overview: https://www.tiny.cloud/docs/advanced/events/ -->

<template>
    <div class="editor-container" >
        <textarea :id="id" :placeholder="placeholder"/>
    </div>
</template>

<script>
import tinymce from 'tinymce/tinymce'
import 'tinymce/themes/modern/theme'

/* Only works with basic lists enabled. */
import 'tinymce/plugins/advlist'
import 'tinymce/plugins/autolink'
import 'tinymce/plugins/autoresize'
import 'tinymce/plugins/autosave'
/* Allows direct manipulation of the html aswell as easy export. */
import 'tinymce/plugins/code'
import 'tinymce/plugins/colorpicker'
import 'tinymce/plugins/fullscreen'
import 'tinymce/plugins/image'
import 'tinymce/plugins/imagetools'
import 'tinymce/plugins/link'
import 'tinymce/plugins/lists'
import 'tinymce/plugins/nonbreaking'
import 'tinymce/plugins/media'
import 'tinymce/plugins/preview'
import 'tinymce/plugins/paste'
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

import 'static/external/tinymce/plugins/placeholder.js'

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
        },
        /* Used to bind the editor to the components text area. */
        id: {
            type: String,
            required: true
        },
        value: {
            type: String,
            default: ''
        },
        placeholder: {
            type: String,
            default: ''
        },
        displayInline: {
            default: false
        },
        minifiedTextArea: {
            default: false
        },
        footer: {
            default: true
        }
    },
    data () {
        return {
            content: '',
            editor: null,
            justFocused: false,
            valueSet: false,
            config: {
                selector: '#' + this.id,
                init_instance_callback: this.editorInit,
                // QUESTION: How the bloody hell do we make this available with webpack so we can use node modules,
                // whilst also predetermining the correct url before bundling?.
                skin_url: '/static/external/tinymce/skins/lightgray',

                paste_data_images: true,
                /* https://www.tiny.cloud/docs/configure/file-image-upload/#images_dataimg_filter
                 * Disables conversion of base64 images into blobs, only used when pasting an image. */
                images_dataimg_filter: function (img) {
                    return img.hasAttribute('internal-blob')
                },

                menubar: true,
                branding: false,
                statusbar: true,
                inline: false,
                image_title: true,

                autosave_ask_before_unload: true,
                autosave_interval: '10s',
                autosave_restore_when_empty: true,
                autoresize_min_height: 150,
                autoresize_max_height: 400,
                autoresize_bottom_margin: 10,

                /* Custom styling applied to the editor */
                content_style: `
                    @import url('https://fonts.googleapis.com/css?family=Roboto+Condensed|Roboto:400,700');
                    body {
                        font-family: 'Roboto Condensed', sans-serif;
                        font-size: 16px !important;
                    }
                `,

                file_picker_types: 'image',
                file_picker_callback: this.insertDataURL,

                placeholder_attrs: {
                    style: {
                        position: 'absolute',
                        top: '19px',
                        left: 13,
                        color: '#888',
                        padding: '1%',
                        width: '98%',
                        overflow: 'hidden',
                        'font-family': 'Roboto Condensed',
                        'white-space': 'pre-wrap'
                    }
                }
            },
            basicConfig: {
                toolbar1: 'bold italic underline alignleft aligncenter alignright alignjustify | forecolor backcolor restoredraft | formatselect | bullist numlist | image media table | removeformat fullscreentoggle fullscreen',
                plugins: [
                    'placeholder autoresize paste textcolor image lists wordcount autolink autosave',
                    'table media fullscreen'
                ]
            },
            extensiveConfig: {
                toolbar1: 'bold italic underline alignleft aligncenter alignright alignjustify | forecolor backcolor | formatselect | bullist numlist | image media table | removeformat fullscreentoggle fullscreen',
                plugins: [
                    'placeholder link media preview paste print hr lists advlist wordcount autolink autosave',
                    'autoresize code fullscreen image imagetools',
                    'textcolor searchreplace table toc'
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
            },
            fullScreenButton: null
        }
    },
    watch: {
        content (value) {
            this.$emit('input', value)
        },
        value (value) {
            this.initValue(value)
        }
    },
    methods: {
        initValue (value) {
            if (value && this.editor && !this.valueSet && (value !== this.content)) {
                let separatedContent = ''
                if (this.content) {
                    separatedContent = this.content.startsWith('<p>') ? this.content : `<p>${this.content}</p>`
                }
                this.content = `${value}${separatedContent}`
                this.editor.setContent(`${value}${separatedContent}`)
                this.valueSet = true
            }
        },
        editorInit (editor) {
            var vm = this
            this.editor = editor

            if (this.displayInline) { this.setupInlineDisplay(editor) }

            editor.on('Change', (e) => { vm.content = this.editor.getContent() })

            editor.on('KeyUp', (e) => {
                vm.handleShortCuts(e)
                vm.content = this.editor.getContent()
            })

            vm.initValue(vm.value)
        },
        setupInlineDisplay (editor) {
            var vm = this

            editor.theme.panel.find('toolbar')[0].$el.hide()
            if (!this.basic) { editor.theme.panel.find('menubar')[0].$el.hide() }
            if (this.footer) { editor.theme.panel.find('#statusbar')[0].$el.hide() }

            editor.on('focus', function () {
                vm.justFocused = true
                setTimeout(() => { vm.justFocused = false }, 20)
                if (!vm.basic) { editor.theme.panel.find('menubar')[0].$el.show() }
                editor.theme.panel.find('toolbar')[0].$el.show()
                if (this.footer) { editor.theme.panel.find('#statusbar')[0].$el.show() }
            })

            editor.on('blur', function () {
                if (vm.justFocused) { return }
                if (!vm.basic) { editor.theme.panel.find('menubar')[0].$el.hide() }
                editor.theme.panel.find('toolbar')[0].$el.hide()
                if (this.footer) { editor.theme.panel.find('#statusbar')[0].$el.hide() }
            })
        },
        handleShortCuts (e) {
            if (this.editor.plugins.fullscreen.isFullscreen() && e.key === 'Escape') {
                this.editor.execCommand('mceFullScreen', {skip_focus: true})
            }
        },
        insertDataURL () {
            var input = document.createElement('input')
            input.setAttribute('type', 'file')
            input.setAttribute('accept', 'image/*')
            var vm = this

            input.onchange = function () {
                var files = this.files
                if (!files.length) { return }

                var file = files[0]
                if (files[0].size > vm.$root.maxFileSizeBytes) {
                    this.$toasted.error('The selected image exceeds the maximum file size of ' + vm.$root.maxFileSizeBytes + ' bytes.')
                    return
                }

                var reader = new FileReader()
                reader.onload = function () {
                    var dataURL = reader.result
                    vm.editor.insertContent('<img src="' + dataURL + '"/>')
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
        minifyTextArea () {
            this.config.autoresize_min_height = 0
            this.config.autoresize_max_height = 150
            this.config.autoresize_bottom_margin = 0.1
            this.config.placeholder_attrs.style.left = 6
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
        },
        /* NOTE: Called from parent. */
        clearContent () {
            this.editor.setContent('')
            this.editor.execCommand('fontName', false, 'Roboto Condensed', {skip_focus: true})
            this.content = ''
        }
    },
    mounted () {
        this.config.statusbar = this.footer

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

        if (this.minifiedTextArea) { this.minifyTextArea() }

        this.enableTabs()
        this.enableBrowserSpellchecker()
        this.enableMarkdownPatterns()

        tinymce.init(this.config)
    },
    beforeDestroy () {
        if (this.editor) { this.editor.destroy() }
    }
}
</script>

<style lang="sass">
.editor-container
    padding-right: 1px
    width: 100%

div.mce-fullscreen
    padding-top: 70px

.modal .mce-fullscreen
    padding-top: 0px
</style>
