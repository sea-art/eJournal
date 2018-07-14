<!--
    Editor for the currently selected preset in the format editor.
    Edits the preset prop directly.
    Various (many!) elements emit a changed event to track whether unsaved changes exist.
-->

<template>
    <div>
        <b-row>
            <b-col cols="12">
                <b-card class="main-card no-hover" :class="$root.getBorderClass($route.params.cID)">
                    <b-row>
                        <b-col cols="9" lg-cols="12">
                            <h2>Preset Deadline</h2>
                            <b-input class="mb-2 mr-sm-2 mb-sm-0" v-model="deadlineDate" type="date" @change="$emit('changed')"/>
                            <br/>
                            <b-input class="mb-2 mr-sm-2 mb-sm-0" v-model="deadlineTime" type="time" @change="$emit('changed')"/>
                            <br/>

                            <h2>Preset Type</h2>
                            <b-form-select v-model="currentPreset.type" @change="onChangePresetType">
                                <option :value="'d'">Entry</option>
                                <option :value="'p'">Progress Check</option>
                            </b-form-select>
                            <br/>
                            <br/>

                            <div v-if="currentPreset.type === 'd'">
                                <h2>Preset Template</h2>
                                <b-form-select v-model="currentPreset.template" @change="$emit('changed')">
                                    <option disabled value="">Please select a template</option>
                                    <option v-for="template in templates" :key="template.t.tID" :value="template.t">
                                        {{template.t.name}}
                                    </option>
                                </b-form-select>
                                <br><br>
                                <div v-if="currentPreset !== null">
                                    <h2>Preview</h2>
                                    <template-preview :template="currentPreset.template"/>
                                </div>
                            </div>
                            <div v-else-if="currentPreset.type === 'p'">
                                <h2>Point Target</h2>
                                <b-input class="mb-2 mr-sm-2 mb-sm-0" v-model="currentPreset.target" placeholder="Amount of points" @change="$emit('changed')"/>
                            </div>
                        </b-col>
                        <b-col cols="3" lg-cols="12">
                            <b-button @click.prevent="emitDeletePreset" class="delete-button float-right">Delete</b-button>
                        </b-col>
                    </b-row>
                </b-card>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import templatePreview from '@/components/template/TemplatePreview.vue'

export default {
    props: ['currentPreset', 'templates'],

    data () {
        return {
            templateNames: []
        }
    },

    // Get/set for the preset deadline.
    computed: {
        deadlineDate: {
            get: function () { return this.currentPreset.deadline.split(' ')[0] },
            set: function (val) { this.currentPreset.deadline = val + ' ' + this.currentPreset.deadline.split(' ')[1]; this.$emit('deadline-changed') }
        },
        deadlineTime: {
            get: function () { return this.currentPreset.deadline.split(' ')[1] },
            set: function (val) { this.currentPreset.deadline = this.currentPreset.deadline.split(' ')[0] + ' ' + val; this.$emit('deadline-changed') }
        }
    },

    methods: {
        emitDeletePreset () {
            this.$emit('changed')
            if (confirm('Are you sure you wish to delete this preset?')) {
                this.$emit('delete-preset')
            }
        },
        // Type-specific fields should be set or deleted
        onChangePresetType (value) {
            this.$emit('changed')
            if (value !== 'p') {
                this.currentPreset.target = ''
            }
            if (value === 'd') {
                if (this.templates[0]) {
                    this.$set(this.currentPreset, 'template', this.templates[0].t)
                } else {
                    this.$set(this.currentPreset, 'template', {})
                }
            }
        }
    },

    components: {
        'template-preview': templatePreview
    }
}
</script>
