<template>
    <div>
        <ckeditor
            v-model="editorData"
            :editor="editor"
            :config="editorConfig"
            @ready="editorInstanceReady"
        />
        <!-- TODO FILE: make this look great -->
        <p v-if="wordCount">
            {{ nWords }} WORDS
        </p>
        <b-button
            @click="test"
        >
            Test
        </b-button>
    </div>
</template>

<script>
import classicEditor from '@ckeditor/ckeditor5-editor-classic/src/classiceditor'

/* Clipboard, Enter, ShiftEnder, Typing, Undo */
import essentialsPlugin from '@ckeditor/ckeditor5-essentials/src/essentials'

/* Basic text styles */
import boldPlugin from '@ckeditor/ckeditor5-basic-styles/src/bold'
import codePlugin from '@ckeditor/ckeditor5-basic-styles/src/code'
import italicPlugin from '@ckeditor/ckeditor5-basic-styles/src/italic'
import strikethroughPlugin from '@ckeditor/ckeditor5-basic-styles/src/strikethrough'
import subscriptPlugin from '@ckeditor/ckeditor5-basic-styles/src/subscript'
import superscriptPlugin from '@ckeditor/ckeditor5-basic-styles/src/superscript'
import underlinePlugin from '@ckeditor/ckeditor5-basic-styles/src/underline'

import alignmentPlugin from '@ckeditor/ckeditor5-alignment/src/alignment'
/* # -> Header 1, `<code>` for inline code etc */
import autoformatPlugin from '@ckeditor/ckeditor5-autoformat/src/autoformat'
/* FontFamily, FontSize, FontColor, FontBackGroundColor */
import fontPlugin from '@ckeditor/ckeditor5-font/src/font'
import headingPlugin from '@ckeditor/ckeditor5-heading/src/heading'
import horizontalLinePlugin from '@ckeditor/ckeditor5-horizontal-line/src/horizontalline'

import imagePlugin from '@ckeditor/ckeditor5-image/src/image'
import imageuploadPlugin from '@ckeditor/ckeditor5-image/src/imageupload'
import imagestylePlugin from '@ckeditor/ckeditor5-image/src/imagestyle'
import imageresizePlugin from '@ckeditor/ckeditor5-image/src/imageresize'

import linkPlugin from '@ckeditor/ckeditor5-link/src/link'
import listPlugin from '@ckeditor/ckeditor5-list/src/list'
import mediaEmbedPlugin from '@ckeditor/ckeditor5-media-embed/src/mediaembed'
import paragraphPlugin from '@ckeditor/ckeditor5-paragraph/src/paragraph'
import pageBreakPlugin from '@ckeditor/ckeditor5-page-break/src/pagebreak'
import pasteFromOfficePlugin from '@ckeditor/ckeditor5-paste-from-office/src/pastefromoffice'
import tablePlugin from '@ckeditor/ckeditor5-table/src/table'
import tableToolbarPlugin from '@ckeditor/ckeditor5-table/src/tabletoolbar'
import wordcountPlugin from '@ckeditor/ckeditor5-word-count/src/wordcount'

import upload from '@/helpers/ckeditor/upload.js'

export default {
    name: 'RichTextEditor',
    props: {
        wordCount: {
            type: Boolean,
            default: false,
        },
        placeholder: {
            type: String,
            default: '',
        },
    },
    data () {
        return {
            editor: classicEditor,
            instance: null,
            editorData: '',
            toolbarGroups: {
                text: ['bold', 'italic', 'underline', 'strikethrough', 'code'],
                alignment: ['alignment:left', 'alignment:right', 'alignment:center', 'alignment:justify'],
                font: ['fontFamily', 'fontSize', 'fontColor', 'fontBackgroundColor'],
                list: ['bulletedList', 'numberedList'],
                actions: ['undo', 'redo'],
                media: ['link', 'mediaEmbed'],
                script: ['subscript', 'superscript'],
                table: ['insertTable', 'tableColumn', 'tableRow', 'mergeTableCells'],
                separation: ['horizontalLine', 'pageBreak'],
                image: ['imageTextAlternative', 'imageStyle:full', 'imageStyle:side', 'imageUpload'],
            },
            editorConfig: {
                plugins: [
                    essentialsPlugin,

                    boldPlugin,
                    codePlugin,
                    italicPlugin,
                    strikethroughPlugin,
                    subscriptPlugin,
                    superscriptPlugin,
                    underlinePlugin,

                    alignmentPlugin,
                    autoformatPlugin,
                    fontPlugin,
                    headingPlugin,
                    horizontalLinePlugin,

                    imagePlugin,
                    imagestylePlugin,
                    imageuploadPlugin,
                    upload.uploadAdapterPlugin,
                    imageresizePlugin,

                    linkPlugin,
                    listPlugin,
                    mediaEmbedPlugin,
                    paragraphPlugin,
                    pageBreakPlugin,
                    pasteFromOfficePlugin,
                    tablePlugin,
                    tableToolbarPlugin,
                    wordcountPlugin,
                ],
                toolbar: {
                    items: [
                        'heading', '|',
                        'bold', 'italic', 'underline', 'strikethrough', 'code', '|',
                        'alignment',
                        'bulletedList',
                        'insertTable', '|',
                        'imageUpload', 'imageStyle:full', 'imageStyle:side', '|',
                        'mediaEmbed', 'link',
                    ],
                },
                wordCount: {
                    displayCharacters: false,
                    displayWords: true,
                    onUpdate: (stats) => {
                        this.nWords = stats.words
                        this.nChars = stats.characters
                    },
                },
            },
            nWords: null,
            nChars: null,
        }
    },
    methods: {
        editorInstanceReady (editorInstance) {
            this.instance = editorInstance
        },
        test () {
            this.editorData = ''
        },
        /* NOTE: Called from parent. */
        clearContent () {
            this.editorData = ''
        },
    },
}
</script>
