<!--
    Format Editor view.
    Lists all templates used within the assignment.
    Template availability for adding by the student can be toggled on a per-template basis.
    Presets are given in a list format, same as the journal view.
-->

<template>
    <b-row class="outer-container-edag-page" no-gutters>
        <b-col md="12" lg="8" xl="9" class="inner-container-edag-page">
            <b-col md="12" lg="auto" xl="4" class="left-content-edag-page">
                <bread-crumb v-if="$root.lgMax()" class="main-content">&nbsp;</bread-crumb>
                <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes" :isInEditFormatPage="true"/>
            </b-col>

            <b-col md="12" lg="auto" xl="8" class="main-content-edag-page">
                <bread-crumb v-if="$root.xl()" class="main-content">&nbsp;</bread-crumb>
                <!--
                    Fill in the template using the corresponding data
                    of the entry
                . -->

                <div v-if="nodes.length > 0">
                    <selected-node-card
                        ref="entry-template-card"
                        :currentPreset="nodes[currentNode]"
                        :templates="templatePool"
                        @deadline-changed="sortList"
                        @delete-preset="deletePreset"
                        @changed="isChanged = true"/>
                </div>
                <div v-else>
                    <p>No presets yet</p>
                </div>

                <b-modal
                    ref="modal"
                    size="lg"
                    ok-only
                    hide-header>
                        <span slot="modal-ok">Back</span>
                        <template-editor :template="templateBeingEdited">
                        </template-editor>
                </b-modal>
            </b-col>
        </b-col>

        <b-col md="12" lg="4" xl="3" class="right-content-edag-page right-content">
            <h3>Format</h3>
            <b-card @click.prevent.stop="addNode" class="hover add-button" :class="'grey-border'">
                <b>+ Add Preset to Format</b>
            </b-card>
            <b-card class="no-hover">
                <b>Point Maximum</b>
                <input class="theme-input" v-model="max_points" placeholder="Point Maximum" type="number">
            </b-card>
            <b-card @click.prevent.stop="saveFormat" class="hover add-button" :class="'grey-border'">
                <b>Save Format</b>
            </b-card>
            <br/>

            <h3>Template Pool</h3>
            <template-todo-card class="hover" v-for="template in templatePool" :key="template.t.tID" @click.native="showModal(template)" :template="template" @delete-template="deleteTemplate"/>
            <b-card @click="showModal(newTemplate())" class="hover add-button" :class="'grey-border'">
                <b>+ Add Template</b>
            </b-card>
        </b-col>
    </b-row>

</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import edag from '@/components/edag/Edag.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import formatEditAvailableTemplateCard from '@/components/format/FormatEditAvailableTemplateCard.vue'
import formatEditSelectTemplateCard from '@/components/format/FormatEditSelectTemplateCard.vue'
import journalAPI from '@/api/journal.js'
import templateEdit from '@/components/template/TemplateEdit.vue'

export default {
    name: 'FormatEdit',

    props: ['cID', 'aID', 'editedTemplate'],

    /* Main data representations:
       templates, presets, unused templates: as received.
       templatePool: the list of used templates. Elements are meta objects with a t field storing the template,
            available field storing student availability, boolean updated field.
       nodes: processed copy of presets.
       deletedTemplates, deletedPresets: stores deleted objects for db communication
       isChanged: stores whether the user has made any changes
    */
    data () {
        return {
            currentNode: 0,

            templates: [],
            presets: [],
            unused_templates: [],

            templatePool: [],
            nodes: [],

            isChanged: false,

            templateBeingEdited: {
                'fields': [],
                'name': '',
                'tID': -1
            },
            wipTemplateId: -1,

            deletedTemplates: [],
            deletedPresets: [],

            max_points: 0
        }
    },

    created () {
        journalAPI.get_format(this.aID)
            .then(data => {
                this.templates = data.format.templates
                this.max_points = data.format.max_points
                this.presets = data.format.presets
                this.unused_templates = data.format.unused_templates
                this.convertFromDB()
            })
            .then(_ => { this.isChanged = false })

        window.addEventListener('beforeunload', e => {
            if (this.$route.name === 'FormatEdit' && this.isChanged) {
                var dialogText = 'Unsaved changes will be lost if you leave. Do you wish to continue?'
                e.returnValue = dialogText
                return dialogText
            }
        })
    },

    watch: {
        templatePool: {
            handler: function () { this.isChanged = true },
            deep: true
        }
    },

    methods: {
        deletePreset () {
            if (typeof this.nodes[this.currentNode].pID !== 'undefined') {
                this.deletedPresets.push(this.nodes[this.currentNode])
            }
            this.nodes.splice(this.currentNode, 1)
            this.currentNode = Math.min(this.currentNode, this.nodes.length - 1)
        },
        deleteTemplate (template) {
            if (typeof template.t.tID !== 'undefined') {
                this.deletedTemplates.push(template.t)
            }
            this.templatePool.splice(this.templatePool.indexOf(template), 1)
        },
        // Used to sort the list when dates are changed. Updates the currentNode index accordingly
        sortList () {
            var temp = this.nodes[this.currentNode]
            this.nodes.sort((a, b) => { return new Date(a.deadline) - new Date(b.deadline) })
            this.currentNode = this.nodes.indexOf(temp)
        },
        newTemplate () {
            return {
                t: {
                    'fields': [],
                    'name': '',
                    'tID': this.wipTemplateId--
                },
                available: false
            }
        },
        // Shows the modal AND sets updated flag on template
        showModal (template) {
            template.updated = true
            if (!this.templatePool.includes(template)) {
                this.templatePool.push(template)
            }
            this.templateBeingEdited = template.t
            this.$refs['modal'].show()
        },
        selectNode ($event) {
            if ($event === this.currentNode) {
                return
            }

            this.currentNode = $event
        },
        newDate () {
            return new Date().toISOString().split('T')[0].slice(0, 10) + ' ' + new Date().toISOString().split('T')[1].slice(0, 5)
        },
        addNode () {
            if (this.nodes.length === 0) {
                this.nodes.push({
                    'type': 'p',
                    'deadline': this.newDate(),
                    'target': 0
                })
                this.isChanged = true
                return
            }

            var newNode = {
                'type': this.nodes[this.currentNode].type,
                'deadline': this.nodes[this.currentNode].deadline
            }

            if (newNode.type === 'd') {
                this.$set(newNode, 'template', this.nodes[this.currentNode].template)
            } else {
                this.$set(newNode, 'target', this.nodes[this.currentNode].target)
            }

            this.nodes.push(newNode)
            this.currentNode = this.nodes.indexOf(newNode)
            this.sortList()
            this.isChanged = true
        },
        // Do client side validation and save to DB
        saveFormat () {
            var invalidDate = false
            var invalidTemplate = false
            var invalidTarget = false

            var lastTarget
            var targetsOutOfOrder = false

            var templatePoolIds = []
            for (var template of this.templatePool) {
                templatePoolIds.push(template.t.tID)
            }
            for (var node of this.nodes) {
                if (!targetsOutOfOrder && node.type === 'p') {
                    if (lastTarget && node.target < lastTarget) {
                        targetsOutOfOrder = true
                        this.$toasted.error('Some preset targets are out of order. Please check the format and try again.')
                    }
                    lastTarget = node.target
                }

                if (!invalidDate && isNaN(Date.parse(node.deadline))) {
                    invalidDate = true
                    this.$toasted.error('One or more presets has an invalid deadline. Please check the format and try again.')
                }
                if (!invalidTemplate && node.type === 'd' && typeof node.template.tID === 'undefined') {
                    invalidTemplate = true
                    this.$toasted.error('One or more presets has an invalid template. Please check the format and try again.')
                }
                if (!invalidTemplate && node.type === 'd' && node.template.tID && !templatePoolIds.includes(node.template.tID)) {
                    invalidTemplate = true
                    this.$toasted.error('One or more presets has an invalid template. Please check the format and try again.')
                }
                if (!invalidTarget && node.type === 'p' && isNaN(parseInt(node.target))) {
                    invalidTarget = true
                    this.$toasted.error('One or more presets has an invalid target. Please check the format and try again.')
                }
                if (!invalidTarget && node.type === 'p' && isNaN(parseInt(node.target))) {
                    invalidTarget = true
                    this.$toasted.error('One or more presets has an invalid target. Please check the format and try again.')
                }
            }

            if (invalidDate | invalidTemplate | invalidTarget | targetsOutOfOrder) {
                return
            }

            this.convertToDB()
            journalAPI.update_format(this.aID, this.templates, this.max_points, this.presets, this.unused_templates, this.deletedTemplates, this.deletedPresets)
                .then(data => {
                    this.templates = data.format.templates
                    this.presets = data.format.presets
                    this.unused_templates = data.format.unused_templates
                    this.deletedTemplates = []
                    this.deletedPresets = []
                    this.convertFromDB()
                })
                .then(_ => {
                    this.isChanged = false
                    this.$toasted.success('New format saved')
                })
        },
        customisePage () {
            this.$toasted.info('Wishlist: Customise page')
        },
        // Utility func to translate from db format to internal
        convertFromDB () {
            var idInPool = []
            var tempTemplatePool = {}

            for (var template of this.templates) {
                idInPool.push(template.tID)
                tempTemplatePool[template.tID] = { t: template, available: true }
            }
            for (var preset of this.presets) {
                if (preset.type === 'd') {
                    if (!idInPool.includes(preset.template.tID)) {
                        idInPool.push(preset.template.tID)
                        tempTemplatePool[preset.template.tID] = { t: preset.template, available: false }
                    } else {
                        preset.template = tempTemplatePool[preset.template.tID].t
                    }
                }
            }
            for (var unusedTemplate of this.unused_templates) {
                idInPool.push(unusedTemplate.tID)
                tempTemplatePool[unusedTemplate.tID] = { t: unusedTemplate, available: false }
            }

            this.templatePool = Object.values(tempTemplatePool).sort((a, b) => { return a.t.tID - b.t.tID })

            this.nodes = this.presets.slice()
            this.nodes.sort((a, b) => { return new Date(a.deadline) - new Date(b.deadline) })
        },
        // Utility func to translate from internal format to db
        convertToDB () {
            this.presets = this.nodes.slice()

            this.templates = []
            this.unused_templates = []

            for (var template of this.templatePool) {
                template.t.updated = template.updated
                if (template.available) {
                    this.templates.push(template.t)
                } else {
                    this.unused_templates.push(template.t)
                }
            }
        }
    },

    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'edag': edag,
        'template-todo-card': formatEditAvailableTemplateCard,
        'selected-node-card': formatEditSelectTemplateCard,
        'template-editor': templateEdit
    },

    // Prompts user
    beforeRouteLeave (to, from, next) {
        if (this.isChanged && !confirm('Unsaved changes will be lost if you leave. Do you wish to continue?')) {
            next(false)
            return
        }

        next()
    }
}
</script>

<style lang="sass">
@import '~sass/partials/edag-page-layout.sass'
</style>
