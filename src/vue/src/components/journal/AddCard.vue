<!--
    Shows the functionality of an Add-Node. It will give the user options
    to select an Entry-Template, this was set by the teacher, and then fill in
    this corresponding Entry-Template so it can be saved and added to the
    Timeline-Tree.
-->
<template>
    <b-card
        :class="$root.getBorderClass($route.params.cID)"
        class="no-hover"
    >
        <div v-if="addNode.templates.length > 1">
            <h2 class="mb-2">
                Select a template
            </h2>
            <b-form-select v-model="selectedTemplate">
                <option
                    :value="null"
                    disabled
                >
                    Please select a template
                </option>
                <option
                    v-for="template in addNode.templates"
                    :key="template.id"
                    :value="template"
                >
                    {{ template.name }}
                </option>
            </b-form-select>
            <br/><br/>
            <entry-preview
                v-if="selectedTemplate !== null"
                ref="entry-prev"
                :template="selectedTemplate"
                :nodeID="addNode.nID"
                @content-template="createEntry"
            />
        </div>
        <div v-else-if="addNode.templates.length === 1">
            <h2 class="mb-2">
                Selected template
            </h2>
            <entry-preview
                ref="entry-prev"
                :template="selectedTemplate"
                :nodeID="addNode.nID"
                @content-template="createEntry"
            />
        </div>
    </b-card>
</template>

<script>
import entryPreview from '@/components/entry/EntryPreview.vue'

export default {
    components: {
        entryPreview,
    },
    props: ['addNode'],
    data () {
        return {
            selectedTemplate: null,
            infoEntry: null,
        }
    },
    created () {
        if (this.addNode.templates.length === 1) {
            this.selectedTemplate = this.addNode.templates[0]
        }
    },
    methods: {
        createEntry (content) {
            this.$emit('info-entry', [this.selectedTemplate, content])
        },
        checkChanges () {
            /* No template is selected, so no changes. */
            if (!this.addNode.templates.length || !this.selectedTemplate) {
                return false
            }

            return this.$refs['entry-prev'].checkChanges()
        },
    },
}
</script>
