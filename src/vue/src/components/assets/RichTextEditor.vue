<template>
    <ckeditor
        v-model="editorData"
        :editor="editor"
        :config="editorConfig"
    />
</template>

<script>
import ClassicEditor from '@ckeditor/ckeditor5-build-classic'

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
            editor: ClassicEditor,
            editorData: '<p>Content of the editor.</p>',
            editorConfig: {
                placeholder: this.placeholder,
                fontFamily: 'Roboto Condensed',
                fontSize: 24
            },
        }
    },
}
</script>

<style lang="sass">
</style>
