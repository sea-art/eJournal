<!--
    Shows the functionality of an Add-Node. It will give the user options
    to select an Entry-Template, this was set by the teacher, and then fill in
    this corresponding Entry-Template so it can be saved and added to the
    EDAG-Tree.
-->
<template>
    <b-card class="card main-card no-hover" :class="$root.getBorderClass($route.params.cID)">
        <b-row>
            <b-col cols="9" lg-cols="12">
                <h2>Select a template</h2>
                <b-form-select v-model="selectedTemplate">
                    <!-- <option :value="null" disabled>Please select a template</option> -->
                    <option v-for="template in addNode.templates" :key="template.tID" :value="template">
                        {{template.name}}
                    </option>
                </b-form-select>
                <br><br>
                <div v-if="selectedTemplate !== null">
                    <entry-preview @content-template="createEntry" :template="selectedTemplate"/>
                </div>
            </b-col>
            <b-col id="main-card-right-column" cols="3" lg-cols="12">
            </b-col>
        </b-row>
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
