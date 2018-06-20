<template>
    <div class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                    <b-card class="card main-card noHoverCard" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <h2>Select a template</h2>
                                <b-form-select v-model="selectedTemplate">
                                    <option :value="null" disabled>Please select a template</option>
                                    <option v-for="template in addNode.templates" :key="template.tID" :value="template">
                                        {{template.name}}
                                    </option>
                                </b-form-select>
                                <br><br>
                                <div v-if="selectedTemplate !== null">
                                    <h3>Preview</h3>
                                    <template-preview :template="selectedTemplate"/>
                                </div>
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
import templatePreview from '@/components/TemplatePreview.vue'

export default {
    props: ['addNode'],

    data () {
        return {
            templateNames: [],
            selectedTemplate: null
        }
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
            this.$emit('add-template', this.selectedTemplate)
        }
    },

    components: {
        'template-preview': templatePreview
    }
}
</script>
