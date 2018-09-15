<template>
    <content-single-column>
        <h1>Welcome to eJournal!</h1>
        <h5>Please enjoy a brief tour of our website:</h5><br/>
        <img src="../../static/landing_page/course_overview.png">
        <img src="../../static/landing_page/journal.png">
        <img src="../../static/landing_page/course_management.png">
        <img src="../../static/landing_page/template_editor.png">
        <img src="../../static/landing_page/format_editor.png">
        <img src="../../static/landing_page/role_configuration.png">
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'

export default {
    name: 'Guest',
    components: {
        'content-single-column': contentSingleColumn
    }
}
</script>
