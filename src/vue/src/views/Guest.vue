<template>
    <content-single-columns>
        <h1>Welcome to eJournal!</h1>
        <text-editor/>
        <h5>Please enjoy a brief tour of our website:</h5><br/>
        <img src="../../static/landing_page/course_overview.png">
        <img src="../../static/landing_page/journal.png">
        <img src="../../static/landing_page/course_management.png">
        <img src="../../static/landing_page/template_editor.png">
        <img src="../../static/landing_page/format_editor.png">
        <img src="../../static/landing_page/role_configuration.png">
    </content-single-columns>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import textEditor from '@/components/assets/TextEditor.vue'

export default {
    name: 'Guest',
    components: {
        'content-single-columns': contentSingleColumn,
        'text-editor': textEditor
    }
}
</script>
