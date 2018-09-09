<!--
    Editor for the currently selected preset in the format editor.
    Edits the preset prop directly.
    Various (many!) elements emit a changed event to track whether unsaved changes exist.
-->

<template>
    <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
        <b-button @click.prevent="emitDeletePreset" class="delete-button float-right multi-form">
            <icon name="trash"/>
            Remove
        </b-button>

        <h2 class="field-heading">Preset Type</h2>
        <b-form-select v-model="currentPreset.type" @change="onChangePresetType" class="multi-form">
            <option value="d">Entry</option>
            <option value="p">Progress Check</option>
        </b-form-select>
        <h2 class="field-heading">Preset Deadline</h2>
        <b-input class="theme-input multi-form" v-model="deadlineDate" type="date" @change="$emit('changed')"/>
        <b-input class="theme-input multi-form" v-model="deadlineTime" type="time" @change="$emit('changed')"/>


        <div v-if="currentPreset.type === 'd'">
            <h2 class="field-heading">Preset Template</h2>
            <b-form-select v-model="currentPreset.template" @change="$emit('changed')" class="multi-form">
                <option disabled value="">Please select a template</option>
                <option v-for="template in templates" :key="template.t.tID" :value="template.t">
                    {{ template.t.name }}
                </option>
            </b-form-select>
            <div v-if="currentPreset !== null">
                <h2 class="field-heading">Preview of the {{ currentPreset.template.name }} template</h2>
                <template-preview :template="currentPreset.template"/>
            </div>
        </div>
        <div v-else-if="currentPreset.type === 'p'">
            <h2 class="field-heading">Point Target</h2>
            <b-input type="number" class="theme-input" v-model="currentPreset.target" placeholder="Amount of points" @change="$emit('changed')"/>
        </div>
    </b-card>
</template>

<script>
import templatePreview from '@/components/template/TemplatePreview.vue'
import icon from 'vue-awesome/components/Icon'

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
            if (confirm('Are you sure you want to remove this preset from this format?')) {
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
        'template-preview': templatePreview,
        icon
    }
}
</script>
