<!--
    Shows the functionality of an Add-Node. It will give the user options
    to select an Entry-Template, this was set by the teacher, and then fill in
    this corresponding Entry-Template so it can be saved and added to the
    EDAG-Tree.
-->
<template>
    <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
        <div v-if="addNode.templates.length > 1">
            <h2 class="mb-2">Select a template</h2>
            <b-form-select v-model="selectedTemplate">
                <option :value="null" disabled>Please select a template</option>
                <option v-for="template in addNode.templates" :key="template.tID" :value="template">
                    {{template.name}}
                </option>
            </b-form-select>
            <br><br>
            <entry-preview v-if="selectedTemplate !== null" @content-template="createEntry" :template="selectedTemplate"/>
        </div>
        <div v-else-if="addNode.templates.length == 1">
            <h2 class="mb-2">Selected template</h2>
            <entry-preview @content-template="createEntry" :template="addNode.templates[0]"/>
        </div>
    </b-card>
</template>

<script>
import templatePreview from '@/components/template/TemplatePreview.vue'
import entryPreview from '@/components/entry/EntryPreview.vue'

export default {
    props: ['addNode'],
    data () {
        return {
            selectedTemplate: null,
            infoEntry: null
        }
    },
    methods: {
        createEntry: function (content) {
            this.$emit('info-entry', [this.selectedTemplate, content])
        }
    },
    components: {
        'template-preview': templatePreview,
        'entry-preview': entryPreview
    }
}
</script>
