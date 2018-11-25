<template>
    <content-single-column>
        <h2>Input to be displayed</h2>
        <textarea v-model="test" class="w-100" @input="injectContent($refs['iframe1'])"/>

        <h2>V-html</h2>
        <div v-html="test"/>

        <h2>Sandboxed iframe</h2>
        <iframe ref="iframe1" @load="test1" id="iframe1" sandbox="allow-same-origin" frameBorder="0" marginwidth="0" marginheight="0" class="w-100" scrolling="no"/>

        <h2>V-html-sanitized</h2>
        <div v-html="$sanitize(test)"/>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'

export default {
    name: 'Test',
    data () {
        return {
            test: '<button onclick="alert(\'hoi\')">Click me</button>'
            // Basic XSS Test Without Filter Evasion
        }
    },
    components: {
        contentSingleColumn
    },
    mounted () {
        this.test1()
        this.injectContent(this.$refs['iframe1'])
    },
    methods: {
        injectContent (obj) {
            var doc = obj.contentWindow.document
            doc.open()
            doc.write(this.test)
            doc.close()
        },
        test1 () {
            this.$refs['iframe1'].height = 21
        }
    }
}
</script>
