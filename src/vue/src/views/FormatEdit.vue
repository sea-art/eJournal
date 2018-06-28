<!--
    Format Editor view.
    Lists all templates used within the assignment.
    Template availability for adding by the student can be toggled on a per-template basis.
    Presets are given in a list format, same as the journal view.
-->

<template>
    <b-row class="outer-container" no-gutters>
        <b-col v-if="bootstrapLg()" cols="12">
            <bread-crumb v-if="bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/>
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
        </b-col>
        <b-col v-else xl="3" class="left-content-format-edit">
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
        </b-col>

        <b-col lg="12" xl="6" order="3" order-xl="2" class="main-content-format-edit">
            <bread-crumb v-if="!bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/>
            <!--
                Fill in the template using the corresponding data
                of the entry
            . -->

            <div v-if="nodes.length > 0">
                <selected-node-card ref="entry-template-card" :currentPreset="nodes[currentNode]" :templates="templatePool" @deadline-changed="sortList" @delete-preset="deletePreset" @changed="isChanged = true" :color="$root.colors[aID % $root.colors.length]"/>
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
        <b-col cols="12" xl="3" order="2" order-xl="3" class="right-content-format-edit">
            <h3>Format</h3>
            <b-card @click.prevent.stop="addNode" class="card hover" :class="'grey-border'" style="">
                <b>+ Add Preset to Format</b>
            </b-card>
            <b-card @click.prevent.stop="saveFormat" class="card hover" :class="'grey-border'" style="">
                <b>Save Format</b>
            </b-card>
            <br/>

            <h3>Template Pool</h3>
            <template-todo-card class="hover" v-for="template in templatePool" :key="template.t.tID" @click.native="showModal(template)" :template="template" @delete-template="deleteTemplate" :color="$root.colors[aID % $root.colors.length]"/>
            <b-card @click="showModal(newTemplate())" class="hover" :class="'grey-border'" style="">
                <b>+ Add Template</b>
            </b-card>
        </b-col>
    </b-row>

</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import edag from '@/components/Edag.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import formatEditAvailableTemplateCard from '@/components/FormatEditAvailableTemplateCard.vue'
import formatEditSelectTemplateCard from '@/components/FormatEditSelectTemplateCard.vue'
import journalAPI from '@/api/journal.js'
import templateEdit from '@/components/TemplateEdit.vue'

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
            windowWidth: 0,
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
            deletedPresets: []
        }
    },

    created () {
        journalAPI.get_format(this.aID)
            .then(data => {
                this.templates = data.format.templates
                this.presets = data.format.presets
                this.unused_templates = data.format.unused_templates
                this.convertFromDB()
            })
            .then(_ => { this.isChanged = false })

        window.addEventListener('beforeunload', e => {
            if (this.$route.name === 'FormatEdit' && this.isChanged) {
                var dialogText = 'Oh no! Unsaved changes will be lost if you leave. Do you wish to continue?'
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
            this.deletedPresets.push(this.nodes[this.currentNode])
            this.nodes.splice(this.currentNode, 1)
        },
        deleteTemplate (template) {
            this.deletedTemplates.push(template.t)
            this.templatePool.splice(this.templatePool.indexOf(template), 1)
        },
        // Used to sort the list when dates are changed. Updates the currentNode index accordingly
        sortList () {
            var temp = this.nodes[this.currentNode]
            this.nodes.sort((a, b) => { return new Date(a.deadline) - new Date(b.deadline) })
            for (var i = 0; i < this.nodes.length; i++) {
                if (this.nodes[i] === temp) {
                    this.currentNode = i
                    break
                }
            }
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
            this.nodes.push({
                'type': 'd',
                'deadline': this.newDate(),
                'template': (this.templatePool[0]) ? this.templatePool[0].t : null
            })
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
            journalAPI.update_format(this.aID, this.templates, this.presets, this.unused_templates, this.deletedTemplates, this.deletedPresets)
                .then(data => {
                    this.templates = data.format.templates
                    this.presets = data.format.presets
                    this.unused_templates = data.format.unused_templates
                    this.deletedTemplates = []
                    this.deletedTemplates = []
                    this.convertFromDB()
                })
                .then(_ => {
                    this.isChanged = false
                    this.$toasted.success('New format saved')
                })
        },
        // Used for responsiveness
        getWindowWidth (event) {
            this.windowWidth = document.documentElement.clientWidth
        },
        // Used for responsiveness
        getWindowHeight (event) {
            this.windowHeight = document.documentElement.clientHeight
        },
        // Used for responsiveness
        bootstrapLg () {
            return this.windowHeight < 1200
        },
        // Used for responsiveness
        bootstrapMd () {
            return this.windowHeight < 922
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

    // Used for responsiveness
    mounted () {
        this.$nextTick(function () {
            window.addEventListener('resize', this.getWindowWidth)

            this.getWindowWidth()
        })
    },

    // Used for responsiveness
    beforeDestroy () {
        window.removeEventListener('resize', this.getWindowWidth)
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
        if (this.isChanged && !confirm('Oh no! Unsaved changes will be lost if you leave. Do you wish to continue?')) {
            next(false)
            return
        }

        next()
    }
}
</script>

<style>
.left-content-format-edit {
    padding: 0px 30px !important;
    flex: 0 0 auto;
}

.main-content-format-edit {
    padding-top: 40px !important;
    background-color: var(--theme-medium-grey);
    flex: 1 1 auto;
    overflow-x: hidden;
}

.right-content-format-edit {
    flex: 0 0 auto;
    padding-top: 30px !important;
    padding-left: 30px !important;
    padding-right: 30px !important;
}

@media (min-width: 1200px) {
    .outer-container {
        height: 100%;
        overflow: hidden;
    }

    .left-content-format-edit {
        height: 100%;
        overflow: hidden;
    }

    .main-content-format-edit, .right-content-format-edit {
        height: 100%;
        overflow-y: scroll;
    }
}

@media (max-width: 1200px) {
    .right-content-format-edit {
        padding: 30px !important;
    }

    .main-content-format-edit {
        padding: 30px !important;
    }
}

@media (max-width: 576px) {
    .left-content-format-edit {
        padding: 0px !important;
    }

    .right-content-format-edit {
        padding: 30px 0px !important;
    }

    .main-content-format-edit {
        padding: 30px 0px !important;
    }
}
</style>
