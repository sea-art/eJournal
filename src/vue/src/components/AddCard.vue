<template>
    <div class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                    <b-card class="card main-card no-hover" :class="'pink-border'">
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
                                    <h3>Fill in your entry</h3>
                                    <entry-preview @content-template="createEntry" :template="selectedTemplate"/>
                                </div>
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
import entryPreview from '@/components/EntryPreview.vue'

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
