<template>
    <div class="editor-container">
        <tiny-mce v-model="content" ref="mce" :init="config"/>
        <div v-html="content"/>
    </div>
</template>

<script>
import 'tinymce/tinymce'
import 'tinymce/themes/modern/theme'
// TODO Figure out why this gives a warning transferred with MIME type
import 'tinymce/skins/lightgray/skin.min.css'
import TinyMCE from '@tinymce/tinymce-vue'

import 'tinymce/plugins/link'
import 'tinymce/plugins/media'
import 'tinymce/plugins/preview'
import 'tinymce/plugins/print'

import 'tinymce/plugins/hr'

export default {
    name: 'TextEditor',
    data () {
        return {
            content: 'Hi',
            config: {
                menubar: true,
                branding: false,
                statusbar: false,

                /* Hides the menu untill selected pop up ontop */
                inline: false,

                menu: {
                    file: {title: 'File', items: 'newdocument preview print'},
                    edit: {title: 'Edit', items: 'undo redo | cut copy paste pastetext | selectall'},
                    insert: {title: 'Insert', items: 'link media | template hr'},
                    view: {title: 'View', items: 'visualaid'},
                    format: {title: 'Format', items: 'bold italic underline strikethrough superscript subscript | formats | removeformat'},
                    table: {title: 'Table', items: 'inserttable tableprops deletetable | cell row column'},
                    tools: {title: 'Tools', items: 'spellchecker code'}
                },
                content_css: ['//fonts.googleapis.com/css?family=Roboto+Condensed|Roboto:400,700'],
                // TODO Figure out why initial render ignores the font
                // font_formats: 'Robot Condensed = roboto condensed',
                // insert_button_items:
                plugins: ['hr', 'link', 'media', 'preview', 'print']
            }
        }
    },
    methods: {
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
