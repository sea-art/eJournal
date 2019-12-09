<!-- Custom wrapper for tinymce editor -->
<!-- If more events are desired, here is an overview: https://www.tiny.cloud/docs/advanced/events/ -->

<template>
    <div
        :ref="`ref-${id}`"
        class="editor-container"
    >
        <!-- <textarea
            :id="id"
            :placeholder="placeholder"
        /> -->
        <div
            :id="id"
            :placeholder="placeholder"
        />
    </div>
</template>

<script>
import tinymce from 'tinymce/tinymce'
import 'tinymce/themes/silver'

/* Only works with basic lists enabled. */
import 'tinymce/plugins/advlist'
import 'tinymce/plugins/autolink'
import 'tinymce/plugins/autoresize'
/* Allows direct manipulation of the html aswell as easy export. */
import 'tinymce/plugins/code'
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
import 'tinymce/plugins/textpattern'
/* Table of contents. */
import 'tinymce/plugins/toc'
import 'tinymce/plugins/wordcount'

import 'public/tinymce/plugins/placeholder.js'

// import contentStyle from '!!raw-loader!tinymce/skins/ui/oxide/content.css'
// import contentStyle2 from '!!raw-loader!tinymce/skins/content/default/content.css'
// content_style: contentStyle.toString() + '\n' + contentStyle2.toString(),

export default {
    name: 'TextEditor',
    props: {
        limitedColors: {
            type: Boolean,
            default: false,
        },
        basic: {
            type: Boolean,
            default: false,
        },
        /* Used to bind the editor to the components text area. */
        id: {
            type: String,
            required: true,
        },
        value: {
            type: String,
            default: '',
        },
        placeholder: {
            type: String,
            default: '',
        },
        displayInline: {
            default: false,
        },
        minifiedTextArea: {
            default: false,
        },
        footer: {
            default: true,
        },
    },
    data () {
        return {
            content: '',
            editor: null,
            justFocused: false,
            valueSet: false,
            config: {
                selector: `#${this.id}`,
                init_instance_callback: this.editorInit,
                // QUESTION: How the bloody hell do we make this available with webpack so we can use node modules,
                // whilst also predetermining the correct url before bundling?.
                skin_url: '/tinymce/skins/ui/oxide',

                paste_data_images: true,
                /* https://www.tiny.cloud/docs/configure/file-image-upload/#images_dataimg_filter
                 * Disables conversion of base64 images into blobs, only used when pasting an image. */
                images_dataimg_filter (img) {
                    return img.hasAttribute('internal-blob')
                },

                menubar: true,
                branding: false,
                statusbar: true,
                inline: false, // TODO not compatible with tabindex -1 (bootstrap modal)
                image_title: true,
                resize: true, // TODO not working as clean as on v4

                min_height: 260,
                max_height: 500,
                autoresize_bottom_margin: 10,
                // autoresize_overflow_padding: 10, // TODO check if theme can benefit from this setting

                /* Custom style applied to the content of the editor */
                content_css: '/tinymce/content.css',

                file_picker_types: 'image',
                file_picker_callback: this.insertDataURL,

                placeholder_attrs: {
                    style: {
                        position: 'absolute',
                        top: '0px',
                        left: 0,
                        color: '#888',
                        fontsize: '1.2em',
                        padding: '13px 0 0 6px',
                        overflow: 'hidden',
                        'font-family': 'Roboto Condensed',
                        'white-space': 'pre-wrap',
                    },
                },
            },
            basicConfig: {
                toolbar1: 'bold italic underline alignleft aligncenter alignright alignjustify '
                    + '| forecolor backcolor | formatselect | bullist numlist | image media table '
                    + '| removeformat fullscreentoggle fullscreen',
                plugins: [
                    'placeholder autoresize paste image lists wordcount autolink',
                    'table media fullscreen',
                ],
            },
            extensiveConfig: {
                toolbar1: 'bold italic underline alignleft aligncenter alignright alignjustify | forecolor backcolor '
                    + '| formatselect | bullist numlist | image media table | removeformat fullscreentoggle fullscreen',
                plugins: [
                    'placeholder link media preview paste print hr lists advlist wordcount autolink',
                    'autoresize code fullscreen image imagetools',
                    'searchreplace table toc',
                ],
            },
            extensiveConfigMenu: {
                menu: {
                    file: { title: 'File', items: 'newdocument print' },
                    edit: { title: 'Edit', items: 'undo redo | cut copy paste | code | selectall searchreplace' },
                    insert: { title: 'Insert', items: 'image media link | hr | toc' },
                    view: { title: 'View', items: 'preview fullscreen' },
                    format: {
                        title: 'Format',
                        items: 'bold italic underline strikethrough superscript subscript '
                            + '| blockformats align | removeformat',
                    },
                    table: { title: 'Table', items: 'inserttable tableprops deletetable | cell row column' },
                },
            },
            fullScreenButton: null,
        }
    },
    watch: {
        content (value) {
            this.$emit('input', value)
        },
        value (value) {
            this.initValue(value)
        },
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
        }

        if (this.minifiedTextArea) { this.minifyTextArea() }

        this.enableTabs()
        this.enableBrowserSpellchecker()
        this.enableMarkdownPatterns()

        tinymce.init(this.config)
    },
    beforeDestroy () {
        if (this.editor) { this.editor.destroy() }
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
            const vm = this
            this.editor = editor

            if (this.displayInline) { this.setupInlineDisplay(editor) }

            editor.on('Change', () => { vm.content = this.editor.getContent() })

            editor.on('KeyUp', (e) => {
                vm.handleShortCuts(e)
                vm.content = this.editor.getContent()
            })

            vm.initValue(vm.value)
        },
        setupInlineDisplay (editor) {
            // TODO might be source of: blockAfter.js:2 Uncaught ReferenceError: do_not_mitigate_inline_scripts
            // is not defined
            // But could also be due to inline property set
            // Does not occur on firefox
            const container = this.$refs[`ref-${this.id}`]

            container.querySelector('div.tox-editor-header').style.display = 'none'
            if (this.footer) { container.querySelector('div.tox-statusbar').style.display = 'none' }

            editor.on('focus', () => {
                this.justFocused = true
                setTimeout(() => { this.justFocused = false }, 20)
                container.querySelector('div.tox-editor-header').style.display = 'block'
                if (this.footer) { container.querySelector('div.tox-statusbar').style.display = 'flex' }
            })

            editor.on('blur', () => {
                if (this.justFocused) { return }
                container.querySelector('div.tox-editor-header').style.display = 'none'
                if (this.footer) { container.querySelector('div.tox-statusbar').style.display = 'none' }
            })
        },
        handleShortCuts (e) {
            if (this.editor.plugins.fullscreen.isFullscreen() && e.key === 'Escape') {
                this.editor.execCommand('mceFullScreen', { skip_focus: true })
            }
        },
        insertDataURL () {
            const input = document.createElement('input')
            input.setAttribute('type', 'file')
            input.setAttribute('accept', 'image/*')

            input.onchange = () => {
                const files = this.files
                if (!files.length) { return }

                const file = files[0]
                if (files[0].size > this.$root.maxFileSizeBytes) {
                    this.$toasted.error(
                        `The selected image exceeds the maximum file size of ${this.$root.maxFileSizeBytes} bytes.`)
                    return
                }

                const reader = new FileReader()
                reader.onload = () => {
                    const dataURL = reader.result
                    this.editor.insertContent(`<img src="${dataURL}"/>`)
                }
                reader.readAsDataURL(file)
            }
            input.click()
        },
        setCustomColors () {
            /* Enables some basic colors to chose from, inline with the websites theme colors. */
            this.config.color_map = [
                '252C39', 'Theme dark blue',
                '007E33', 'Theme positive selected',
                'FF8800', 'Theme change selected',
                'CC0000', 'Theme negative selected',
            ]
            this.config.custom_colors = false
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
            this.config.min_height = 10
            this.config.max_height = 260
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
                { start: '*', end: '*', format: 'italic' },
                { start: '**', end: '**', format: 'bold' },
                { start: '#', format: 'h1' },
                { start: '##', format: 'h2' },
                { start: '###', format: 'h3' },
                { start: '####', format: 'h4' },
                { start: '#####', format: 'h5' },
                { start: '######', format: 'h6' },
                { start: '1. ', cmd: 'InsertOrderedList' },
                { start: '* ', cmd: 'InsertUnorderedList' },
                { start: '- ', cmd: 'InsertUnorderedList' },
            ]
        },
        /* NOTE: Called from parent. */
        clearContent () {
            this.editor.setContent('')
            this.content = ''
        },
    },
}
</script>

<style lang="sass">
.editor-container
    border-radius: 5px !important
    padding-right: 1px
    width: 100%
    div
        border-radius: 5px !important

div.mce-fullscreen
    padding-top: 70px

.modal .mce-fullscreen
    padding-top: 0px
</style>
