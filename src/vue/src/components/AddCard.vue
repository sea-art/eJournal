<template>
    <div class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                    <b-card class="card main-card noHoverCard" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <h2>Select a template a template</h2>
                                <b-form-select v-model="selectedTemplate">
                                    <div v-for="template in templates">
                                        <option value="template">{{template.name}}</option>
                                    </div>
                                </b-form-select>
                                <br>
                                <h3>Preview</h3>
                                <template-preview :template="addNode.templates[0]"/>
                                <br>
                                <b-button @click="addTemplate">Add template</b-button>
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12">
                            </b-col>
                        </b-row>
                    </b-card>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import templatePreview from '@/components/templatePreview.vue'

export default {
    props: ['addNode'],

    data () {
        templateNames: []
        selectedTemplate: addNode.templates[0]
    },

    created () {
        this.fillTemplateNames()
    },

    methods: {
        fillTemplateNames: function () {
            for (var template of this.addNode.templates) {
                this.templateNames.push(template.name)
            }
        },
        addTemplate: function () {
            this.$emit('edit-data', this.selectedTemplate)
        }
    },

    components: {
        'template-preview': templatePreview
    }
}
</script>
