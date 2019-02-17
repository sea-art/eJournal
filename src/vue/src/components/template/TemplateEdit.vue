<template>
    <b-card class="no-hover">
        <div class="d-flex">
            <b-button
                @click="mode = 'edit'"
                class="multi-form change-button flex-basis-100"
                :class="{'active': mode === 'edit'}">
                <icon name="edit"/>
                Edit
            </b-button>
            <b-button
                @click="mode='preview'"
                class="multi-form add-button flex-basis-100"
                :class="{'active': mode === 'preview'}">
                <icon name="eye"/>
                Preview
            </b-button>
        </div>
        <hr/>
        <div v-if="this.mode == 'edit'">
            <b-card class="no-hover">
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" id="template-name" v-model="template.name" placeholder="Template name" required/>
                <div v-if="!formatSettings.available" class="template-availability">
                    <b-button v-on:click.stop @click="toggleActive" class="delete-button">
                        <icon name="times"/>
                        Preset-only
                    </b-button>
                    <icon name="info-circle"/>
                    This template can only be used for preset entries you add to the timeline
                </div>
                <div v-if="formatSettings.available" class="template-availability">
                    <b-button v-on:click.stop @click="toggleActive" class="add-button">
                        <icon name="check"/>
                        Unlimited
                    </b-button>
                    <icon name="info-circle"/>
                    This template can be freely used by students as often as they want<br/>
                </div>
            </b-card>
            <draggable v-model="template.field_set" @start="startDrag" @end="endDrag" @update="onUpdate" :options="{ handle:'.handle' }">
                <b-card v-for="field in template.field_set" :key="field.location" class="field-card">
                    <b-row align-h="between" no-gutters>
                        <b-col cols="12" sm="10" lg="11">
                            <b-input class="multi-form theme-input" v-model="field.title" placeholder="Field title" required/>
                            <text-editor
                                class="multi-form"
                                v-if="showEditors"
                                :id="`rich-text-editor-field-${template.id}-${field.location}`"
                                :basic="true"
                                :footer="false"
                                :givenContent="field.description ? field.description : ''"
                                @content-update="field.description = $event"
                                required
                            />
                            <div class="d-flex">
                                <b-select class="multi-form mr-2" :options="fieldTypes" v-model="field.type" @change="field.options = ''"></b-select>
                                <b-button v-on:click.stop v-if="!field.required" @click="field.required = !field.required" class="optional-field-template float-right multi-form">
                                    <icon name="asterisk"/>
                                    Optional
                                </b-button>
                                <b-button v-on:click.stop v-if="field.required" @click="field.required = !field.required" class="required-field-template float-right multi-form">
                                    <icon name="asterisk"/>
                                    Required
                                </b-button>
                            </div>

                            <!-- Field Options -->
                            <div v-if="field.type == 's'">
                                <!-- Event targeting allows us to access the input value -->
                                <div class="d-flex">
                                    <b-input class="multi-form mr-2 theme-input" placeholder="Enter an option"
                                    @keyup.enter.native="addSelectionOption($event.target, field)"/>
                                    <b-button class="float-right multi-form"
                                    @click.stop="addSelectionOption($event.target.previousElementSibling, field)">
                                        <icon name="plus"/>
                                        Add option
                                    </b-button>
                                </div>
                                <div v-if="field.options">
                                    <b-button
                                        v-for="(option, index) in JSON.parse(field.options)"
                                        :key="index"
                                        class="delete-button mr-2 mb-2"
                                        @click.stop="removeSelectionOption(option, field)">
                                        <icon name="trash"/>
                                        {{ option }}
                                    </b-button>
                                </div>
                            </div>

                        </b-col>
                        <b-col cols="12" sm="2" lg="1" class="icon-box">
                            <div class="handle d-inline d-sm-block">
                                <icon class="move-icon" name="arrows" scale="1.75"/>
                            </div>
                            <icon class="trash-icon" @click.native="removeField(field.location)" name="trash" scale="1.75"/>
                        </b-col>
                    </b-row>
                </b-card>
                <div class="invisible"></div>
            </draggable>
            <b-button class="add-button full-width" @click="addField">
                <icon name="plus"/>
                Add field
            </b-button>
        </div>
        <template-preview v-else :template="template"/>
    </b-card>
</template>

<script>
import ContentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import TemplatePreview from '@/components/template/TemplatePreview.vue'
import textEditor from '@/components/assets/TextEditor.vue'
import draggable from 'vuedraggable'
import icon from 'vue-awesome/components/Icon'

export default {
    props: {
        template: {
            required: true
        },
        formatSettings: {
            required: true
        }
    },
    data () {
        return {
            fieldTypes: {
                't': 'Text',
                'rt': 'Rich Text',
                'i': 'Image',
                'p': 'PDF',
                'f': 'File',
                'v': 'YouTube Video',
                'u': 'URL',
                'd': 'Date',
                's': 'Selection'
            },
            mode: 'edit',
            selectedLocation: null,
            showEditors: true
        }
    },
    components: {
        'content-single-column': ContentSingleColumn,
        icon,
        'draggable': draggable,
        'text-editor': textEditor,
        'template-preview': TemplatePreview
    },
    methods: {
        updateLocations () {
            for (var i = 0; i < this.template.field_set.length; i++) {
                this.template.field_set[i].location = i
            }
        },
        addField () {
            var newField = {
                'type': 't',
                'title': '',
                'description': '',
                'options': null,
                'location': this.template.field_set.length,
                'required': true
            }

            this.template.field_set.push(newField)
        },
        removeField (location) {
            if (this.template.field_set[location].title
                ? confirm('Are you sure you want to remove "' + this.template.field_set[location].title + '" from this template?')
                : confirm('Are you sure you want to remove this field from this template?')) {
                this.template.field_set.splice(location, 1)
            }

            this.updateLocations()
        },
        startDrag () {
            this.showEditors = false
        },
        endDrag () {
            this.showEditors = true
        },
        onUpdate () {
            this.updateLocations()
        },
        addSelectionOption (target, field) {
            if (target.value.trim()) {
                if (!field.options) {
                    field.options = JSON.stringify([])
                }
                var options = JSON.parse(field.options)
                options.push(target.value.trim())
                field.options = JSON.stringify(options)
                target.value = ''
                target.focus()
            }
        },
        removeSelectionOption (option, field) {
            var options = JSON.parse(field.options)
            options.splice(options.indexOf(option.trim()), 1)
            field.options = JSON.stringify(options)
        },
        toggleActive () {
            this.formatSettings.available = !this.formatSettings.available
        }
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
@import '~sass/modules/breakpoints.sass'

.optional-field-template
    background-color: white
    color: $theme-dark-blue !important
    svg
        fill: $theme-medium-grey

.required-field-template
    background-color: $theme-dark-blue
    color: white !important
    svg, &:hover:not(.no-hover) svg
        fill: $theme-red !important

#template-name
    font-weight: bold
    font-size: 1.8em
    font-family: 'Roboto', sans-serif
    color: $theme-dark-blue

.field-card
    background-color: $theme-medium-grey

.sortable-chosen .card
    background-color: $theme-dark-grey

.sortable-ghost
    visibility: hidden

.sortable-drag .card
    visibility: visible

.icon-box
    text-align: center

.handle
    text-align: center
    padding-bottom: 7px

.field-card:hover .move-icon, .field-card:hover .trash-icon
    fill: $theme-dark-blue !important

.handle:hover .move-icon
    cursor: grab
    fill: $theme-blue !important

.field-card:hover .trash-icon:hover
    fill: $theme-red !important

@include sm-max
    .icon-box
        margin-top: 10px

.template-availability
    font-weight: bold
    color: grey
    .btn
        margin-right: 20px
        @include md-max
            width: 100%
            margin-bottom: 10px
    svg
        fill: grey
</style>
