<!--
    Format Editor view.
    Lists all templates used within the assignment.
    Template availability for adding by the student can be toggled on a per-template basis.
    Presets are given in a list format, same as the journal view.
-->

<template>
    <b-row
        class="outer-container-timeline-page"
        noGutters
    >
        <b-col
            md="12"
            lg="8"
            xl="9"
            class="inner-container-timeline-page"
        >
            <b-col
                md="12"
                lg="auto"
                xl="4"
                class="left-content-timeline-page"
            >
                <bread-crumb
                    v-if="$root.lgMax"
                    v-intro="'Welcome to the assignment editor!<br/>This is where you can configure the structure of \
                    your assignment. Proceed with this tutorial to learn more.'"
                    v-intro-step="1"
                >
                    <icon
                        v-intro="'That\'s it! If you have any more questions, do not hesitate to contact us via the \
                        feedback button below. This tutorial can be consulted again by clicking the info sign.'"
                        v-intro-step="4"
                        v-b-tooltip.hover
                        name="info"
                        scale="1.5"
                        title="Click to start a tutorial for this page"
                        class="info-icon"
                        @click.native="startTour"
                    />
                </bread-crumb>
                <timeline
                    v-intro="'The timeline forms the basis for an assignment. The name, due date and other details \
                    of the assignment can also be changed here, by clicking the first node.<br/><br/>The timeline \
                    contains a node for every entry. You can add two different types of nodes to it:<br/><br/><ul> \
                    <li><b>Preset entries</b> are entries with a specific template which have to be completed before \
                    a set deadline</li><li><b>Progress goals</b> are point targets that have to be met before a \
                    set deadline</li></ul>New nodes can be added via the \'+\' node. Click any node to view its \
                    contents.'"
                    v-intro-step="3"
                    :selected="currentNode"
                    :nodes="nodes"
                    :edit="true"
                    @select-node="selectNode"
                />
            </b-col>

            <b-col
                md="12"
                lg="auto"
                xl="8"
                class="main-content-timeline-page"
            >
                <bread-crumb
                    v-if="$root.xl"
                    v-intro="'Welcome to the assignment editor!<br/>This is where you can configure the structure of \
                    your assignment. Proceed with this tutorial to learn more.'"
                    v-intro-step="1"
                >
                    <icon
                        v-intro="'That\'s it! If you have any more questions, do not hesitate to contact us via the \
                        feedback button below. This tutorial can be consulted again by clicking the info sign.'"
                        v-intro-step="4"
                        v-b-tooltip.hover
                        name="info"
                        scale="1.75"
                        title="Click to start a tutorial for this page"
                        class="info-icon"
                        @click.native="startTour"
                    />
                </bread-crumb>

                <assignment-details-card
                    v-if="currentNode === -1"
                    :class="{ 'input-disabled' : saveRequestInFlight }"
                    :assignmentDetails="assignmentDetails"
                    :presetNodes="presets"
                    @changed="isChanged = true"
                />

                <preset-node-card
                    v-else-if="nodes.length > 0 && currentNode !== -1 && currentNode < nodes.length"
                    ref="entry-template-card"
                    :class="{ 'input-disabled' : saveRequestInFlight }"
                    :currentPreset="nodes[currentNode]"
                    :templates="templatePool"
                    :assignmentDetails="assignmentDetails"
                    @deadline-changed="sortList"
                    @delete-preset="deletePreset"
                    @changed="isChanged = true"
                />

                <add-preset-node
                    v-else-if="currentNode === nodes.length"
                    :class="{ 'input-disabled' : saveRequestInFlight }"
                    :templates="templatePool"
                    :assignmentDetails="assignmentDetails"
                    @new-preset="newPreset"
                />

                <b-card
                    v-else-if="currentNode === nodes.length + 1"
                    class="no-hover"
                    :class="$root.getBorderClass($route.params.cID)"
                >
                    <h2>End of assignment</h2>
                    <p>This is the end of the assignment.</p>
                </b-card>

                <b-modal
                    ref="templateModal"
                    size="lg"
                    title="Edit template"
                    hideFooter
                >
                    <template-editor
                        :template="templateBeingEdited.t"
                        :formatSettings="templateBeingEdited"
                    />
                </b-modal>
            </b-col>
        </b-col>

        <b-col
            md="12"
            lg="4"
            xl="3"
            class="right-content-timeline-page right-content"
        >
            <div
                v-intro="'Every assignment contains customizable <i>templates</i> which specify what the contents of \
                each journal entry should be. There are two different types of templates:<br/><br/><ul><li><b>\
                Unlimited templates</b> can be freely used by students as often as they want</li><li><b>Preset-only \
                templates</b> can be used only for preset entries that you add to the timeline</li></ul>You can \
                preview and edit a template by clicking on it.'"
                v-intro-step="2"
                :class="{ 'input-disabled' : saveRequestInFlight }"
            >
                <h3>Entry Templates</h3>
                <b-card
                    :class="$root.getBorderClass($route.params.cID)"
                    class="no-hover"
                >
                    <available-template
                        v-for="template in templatePool"
                        :key="template.t.id"
                        :template="template"
                        @edit-template="showTemplateModal(template)"
                        @delete-template="deleteTemplate"
                    />
                </b-card>
                <b-button
                    class="add-button multi-form"
                    @click="showTemplateModal(newTemplate())"
                >
                    <icon name="plus"/>
                    Create New Template
                </b-button>
            </div>
        </b-col>

        <transition name="fade">
            <b-button
                v-if="isChanged"
                :class="{ 'input-disabled' : saveRequestInFlight }"
                class="add-button fab"
                @click.prevent.stop="saveFormat"
            >
                <icon
                    name="save"
                    scale="1.5"
                />
            </b-button>
        </transition>
    </b-row>
</template>

<script>
import timeline from '@/components/timeline/Timeline.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import formatAssignmentDetailsCard from '@/components/format/FormatAssignmentDetailsCard.vue'
import formatAvailableTemplate from '@/components/format/FormatAvailableTemplate.vue'
import formatPresetNodeCard from '@/components/format/FormatPresetNodeCard.vue'
import formatAddPresetNode from '@/components/format/FormatAddPresetNode.vue'
import templateEdit from '@/components/template/TemplateEdit.vue'
import formatAPI from '@/api/format.js'
import preferencesAPI from '@/api/preferences.js'

export default {
    name: 'FormatEdit',
    components: {
        breadCrumb,
        'assignment-details-card': formatAssignmentDetailsCard,
        'available-template': formatAvailableTemplate,
        'preset-node-card': formatPresetNodeCard,
        'add-preset-node': formatAddPresetNode,
        'template-editor': templateEdit,
        timeline,
    },
    props: ['cID', 'aID'],
    /* Main data representations:
       templates, presets, unused templates: as received.
       templatePool: the list of used templates. Elements are meta objects with a t field storing the template,
            available field storing student availability, boolean updated field.
       nodes: processed copy of presets.
       deletedTemplates, deletedPresets: stores deleted objects for db communication
       isChanged: stores whether the user has made any changes
       saveRequestInFlight: stores whether a request to save is in flight, should not allow changes as that would
            create desync between server and local (format is reloaded after save response, local changes lost)
    */
    data () {
        return {
            currentNode: -1,

            assignmentDetails: {},

            templates: [],
            presets: [],
            unusedTemplates: [],

            templatePool: [],
            nodes: [],

            isChanged: false,
            saveRequestInFlight: false,

            templateBeingEdited: {
                t: {
                    field_set: [],
                    name: '',
                    id: -1,
                },
                available: true,
            },
            wipTemplateId: -1,

            deletedTemplates: [],
            deletedPresets: [],
        }
    },
    watch: {
        templatePool: {
            handler () {
                if (!this.saveRequestInFlight) {
                    this.isChanged = true
                }
            },
            deep: true,
        },
    },
    created () {
        formatAPI.get(this.aID)
            .then((data) => {
                this.saveFromDB(data)
                this.convertFromDB()
                if (this.$store.getters['preferences/showFormatTutorial']) {
                    preferencesAPI.update(this.$store.getters['user/uID'], { show_format_tutorial: false })
                        .then(() => { this.$store.commit('preferences/SET_FORMAT_TUTORIAL', false) })
                    this.startTour()
                }
            })
            .then(() => { this.isChanged = false })

        window.addEventListener('beforeunload', (e) => { // eslint-disable-line
            if (this.$route.name === 'FormatEdit' && this.isChanged) {
                const dialogText = 'Unsaved changes will be lost if you leave. Do you wish to continue?'
                e.returnValue = dialogText
                return dialogText
            }
        })
    },
    methods: {
        deletePreset () {
            if (typeof this.nodes[this.currentNode].id !== 'undefined') {
                this.deletedPresets.push(this.nodes[this.currentNode])
            }
            this.nodes.splice(this.currentNode, 1)
            this.currentNode = Math.min(this.currentNode, this.nodes.length - 1)
        },
        deleteTemplate (template) {
            if (typeof template.t.id !== 'undefined') {
                this.deletedTemplates.push(template.t)
            }
            this.templatePool.splice(this.templatePool.indexOf(template), 1)
        },
        // Used to sort the list when dates are changed. Updates the currentNode index accordingly
        sortList () {
            const temp = this.nodes[this.currentNode]
            this.nodes.sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
            this.currentNode = this.nodes.indexOf(temp)
        },
        newTemplate () {
            return {
                t: {
                    field_set: [{
                        type: 'rt',
                        title: 'Entry',
                        description: '',
                        options: null,
                        location: 0,
                        required: true,
                    }],
                    name: 'Untitled Template',
                    id: this.wipTemplateId--,
                },
                available: true,
            }
        },
        // Shows the modal and sets updated flag on template
        showTemplateModal (template) {
            template.updated = true
            if (!this.templatePool.includes(template)) {
                this.templatePool.push(template)
            }
            this.templateBeingEdited = template
            this.$refs.templateModal.show()
        },
        hideModal (ref) {
            this.$refs[ref].hide()
        },
        selectNode ($event) {
            if ($event === this.currentNode) {
                return
            }

            this.currentNode = $event
        },
        newDate () {
            const pre = new Date().toISOString().split('T')[0].slice(0, 10)
            const post = new Date().toISOString().split('T')[1].slice(0, 5)
            return `${pre} ${post}`
        },
        newPreset (presetContent) {
            this.nodes.push(presetContent)
            this.currentNode = this.nodes.indexOf(presetContent)
            this.sortList()
            this.isChanged = true

            this.$toasted.success('Added new preset.')
        },
        // Do client side validation and save to DB
        saveFormat () {
            let missingAssignmentName = false
            let missingPointMax = false
            let unlockAfterDue = false
            let unlockAfterLock = false
            let dueAfterLock = false

            let presetUnlockBeforeUnlock = false
            let presetUnlockAfterDue = false
            let presetUnlockAfterLock = false
            let presetDueBeforeUnlock = false
            let presetDueAfterDue = false
            let presetDueAfterLock = false
            let presetLockBeforeUnlock = false
            let presetLockAfterDue = false
            let presetLockAfterLock = false
            let presetUnlockAfterPresetDue = false
            let presetUnlockAfterPresetLock = false
            let presetDueAfterPresetLock = false

            let presetInvalidDue = false
            let presetInvalidLock = false
            let presetInvalidUnlock = false
            let presetInvalidTemplate = false
            let presetInvalidTarget = false

            let lastTarget
            let targetsOutOfOrder = false

            const templatePoolIds = []
            this.templatePool.forEach((template) => {
                templatePoolIds.push(template.t.id)
            })

            if (!/\S/.test(this.assignmentDetails.name)) {
                missingAssignmentName = true
                this.$toasted.error('Assignment name is missing. Please check the format and try again.')
            }

            if (!missingPointMax && Number.isNaN(parseInt(this.assignmentDetails.points_possible, 10))) {
                missingPointMax = true
                this.$toasted.error('Points possible is missing. Please check the format and try again.')
            }

            if (!unlockAfterDue && this.assignmentDetails.unlock_date && this.assignmentDetails.due_date
                && Date.parse(this.assignmentDetails.unlock_date) > Date.parse(this.assignmentDetails.due_date)) {
                unlockAfterDue = true
                this.$toasted.error(
                    'The assignment is due before the unlock date. Please check the format and try again.')
            }
            if (!unlockAfterLock && this.assignmentDetails.unlock_date && this.assignmentDetails.lock_date
                && Date.parse(this.assignmentDetails.unlock_date) > Date.parse(this.assignmentDetails.lock_date)) {
                unlockAfterLock = true
                this.$toasted.error(
                    'The assignment lock date is before the unlock date. Please check the format and try again.')
            }
            if (!dueAfterLock && this.assignmentDetails.due_date && this.assignmentDetails.lock_date
                && Date.parse(this.assignmentDetails.due_date) > Date.parse(this.assignmentDetails.lock_date)) {
                dueAfterLock = true
                this.$toasted.error(
                    'The assignment lock date is before the due date. Please check the format and try again.')
            }

            this.nodes.forEach((node) => {
                if (!targetsOutOfOrder && node.type === 'p') {
                    if (lastTarget && node.target < lastTarget) {
                        targetsOutOfOrder = true
                        this.$toasted.error(
                            'Some preset targets are out of order. Please check the format and try again.')
                    }
                    lastTarget = node.target
                }

                if (!presetInvalidDue && Number.isNaN(Date.parse(node.due_date))) {
                    presetInvalidDue = true
                    this.$toasted.error(
                        'One or more presets have an invalid due date. Please check the format and try again.')
                }
                if (!presetInvalidLock && node.lock_date && Number.isNaN(Date.parse(node.lock_date))) {
                    presetInvalidLock = true
                    this.$toasted.error(
                        'One or more presets have an invalid lock date. Please check the format and try again.')
                }
                if (!presetInvalidUnlock && node.unlock_date && Number.isNaN(Date.parse(node.unlock_date))) {
                    presetInvalidUnlock = true
                    this.$toasted.error(
                        'One or more presets have an invalid unlock date. Please check the format and try again.')
                }
                if (!presetInvalidTemplate && node.type === 'd' && typeof node.template.id === 'undefined') {
                    presetInvalidTemplate = true
                    this.$toasted.error(
                        'One or more presets have an invalid template. Please check the format and try again.')
                }
                if (!presetInvalidTemplate && node.type === 'd'
                    && node.template.id
                    && !templatePoolIds.includes(node.template.id)) {
                    presetInvalidTemplate = true
                    this.$toasted.error(
                        'One or more presets have an invalid template. Please check the format and try again.')
                }
                if (!presetInvalidTarget && node.type === 'p' && Number.isNaN(parseInt(node.target, 10))) {
                    presetInvalidTarget = true
                    this.$toasted.error(
                        'One or more presets have an invalid target. Please check the format and try again.')
                }

                if (!presetUnlockAfterPresetDue && node.unlock_date && node.due_date
                    && Date.parse(node.unlock_date) > Date.parse(node.due_date)) {
                    presetUnlockAfterPresetDue = true
                    this.$toasted.error(
                        'One or more presets are due before their unlock date. Please check the format and try again.')
                }
                if (!presetUnlockAfterPresetLock && node.unlock_date && node.lock_date
                    && Date.parse(node.unlock_date) > Date.parse(node.lock_date)) {
                    presetUnlockAfterPresetLock = true
                    this.$toasted.error('One or more presets have a lock date before their unlock date. '
                        + 'Please check the format and try again.')
                }
                if (!presetDueAfterPresetLock && node.due_date && node.lock_date
                    && Date.parse(node.due_date) > Date.parse(node.lock_date)) {
                    presetDueAfterPresetLock = true
                    this.$toasted.error('One or more presets have a lock date before their due date. '
                        + 'Please check the format and try again.')
                }

                if (!presetUnlockBeforeUnlock && this.assignmentDetails.unlock_date
                    && Date.parse(node.unlock_date) < Date.parse(this.assignmentDetails.unlock_date)) {
                    presetUnlockBeforeUnlock = true
                    this.$toasted.error('One or more presets have an unlock date before the assignment unlock date. '
                        + 'Please check the format and try again.')
                }
                if (!presetUnlockAfterDue && this.assignmentDetails.due_date
                    && Date.parse(node.unlock_date) > Date.parse(this.assignmentDetails.due_date)) {
                    presetUnlockAfterDue = true
                    this.$toasted.error('One or more presets have an unlock date after the assignment due date. '
                        + 'Please check the format and try again.')
                }
                if (!presetUnlockAfterLock && this.assignmentDetails.lock_date
                    && Date.parse(node.unlock_date) > Date.parse(this.assignmentDetails.lock_date)) {
                    presetUnlockAfterLock = true
                    this.$toasted.error('One or more presets have an unlock date after the assignment lock date. '
                        + 'Please check the format and try again.')
                }
                if (!presetDueBeforeUnlock && this.assignmentDetails.unlock_date
                    && Date.parse(node.due_date) < Date.parse(this.assignmentDetails.unlock_date)) {
                    presetDueBeforeUnlock = true
                    this.$toasted.error('One or more presets have a due date before the assignment unlock date. '
                        + 'Please check the format and try again.')
                }
                if (!presetDueAfterDue && this.assignmentDetails.due_date
                    && Date.parse(node.due_date) > Date.parse(this.assignmentDetails.due_date)) {
                    presetDueAfterDue = true
                    this.$toasted.error('One or more presets have a due date after the assignment due date. '
                        + 'Please check the format and try again.')
                }
                if (!presetDueAfterLock && this.assignmentDetails.lock_date
                    && Date.parse(node.due_date) > Date.parse(this.assignmentDetails.lock_date)) {
                    presetDueAfterLock = true
                    this.$toasted.error('One or more presets have a due date after the assignment lock date. '
                        + 'Please check the format and try again.')
                }
                if (!presetLockBeforeUnlock && this.assignmentDetails.unlock_date
                    && Date.parse(node.lock_date) < Date.parse(this.assignmentDetails.unlock_date)) {
                    presetLockBeforeUnlock = true
                    this.$toasted.error('One or more presets have a lock date before the assignment unlock date. '
                        + 'Please check the format and try again.')
                }
                if (!presetLockAfterDue && this.assignmentDetails.due_date
                    && Date.parse(node.lock_date) > Date.parse(this.assignmentDetails.due_date)) {
                    presetLockAfterDue = true
                    this.$toasted.error('One or more presets have a lock date after the assignment due date. '
                        + 'Please check the format and try again.')
                }
                if (!presetLockAfterLock && this.assignmentDetails.lock_date
                    && Date.parse(node.lock_date) > Date.parse(this.assignmentDetails.lock_date)) {
                    presetLockAfterLock = true
                    this.$toasted.error('One or more presets have a lock date after the assignment lock date. '
                        + 'Please check the format and try again.')
                }
            })

            if (missingAssignmentName || missingPointMax || unlockAfterDue || unlockAfterLock
                || dueAfterLock || presetUnlockBeforeUnlock || presetUnlockAfterDue
                || presetUnlockAfterLock || presetDueBeforeUnlock || presetDueAfterDue
                || presetDueAfterLock || presetLockBeforeUnlock || presetLockAfterDue
                || presetUnlockAfterPresetDue || presetUnlockAfterPresetLock
                || presetDueAfterPresetLock || presetLockAfterLock || presetInvalidDue
                || presetInvalidLock || presetInvalidUnlock || presetInvalidTemplate
                || presetInvalidTarget || targetsOutOfOrder) {
                return
            }
            this.saveRequestInFlight = true
            this.convertToDB()
            formatAPI.update(this.aID, {
                assignment_details: this.assignmentDetails,
                templates: this.templates,
                presets: this.presets,
                unused_templates: this.unusedTemplates,
                removed_templates: this.deletedTemplates,
                removed_presets: this.deletedPresets,
            }, { customSuccessToast: 'New format saved' })
                .then((data) => {
                    this.saveFromDB(data)
                    this.convertFromDB()
                    this.saveRequestInFlight = false
                    this.$nextTick(() => { this.isChanged = false })
                })
                .catch(() => { this.saveRequestInFlight = false })
        },
        saveFromDB (data) {
            this.assignmentDetails = data.assignment_details
            this.templates = data.format.templates
            this.presets = data.format.presets
            this.unusedTemplates = data.format.unused_templates
            this.deletedTemplates = []
            this.deletedPresets = []
        },
        // Utility func to translate from db format to internal
        convertFromDB () {
            const idInPool = []
            const tempTemplatePool = {}

            this.templates.forEach((template) => {
                idInPool.push(template.id)
                tempTemplatePool[template.id] = { t: template, available: true }
            })

            this.presets.forEach((preset) => {
                if (preset.type === 'd') {
                    if (!idInPool.includes(preset.template.id)) {
                        idInPool.push(preset.template.id)
                        tempTemplatePool[preset.template.id] = { t: preset.template, available: false }
                    } else {
                        preset.template = tempTemplatePool[preset.template.id].t
                    }
                }
            })

            this.unusedTemplates.forEach((unusedTemplate) => {
                idInPool.push(unusedTemplate.id)
                tempTemplatePool[unusedTemplate.id] = { t: unusedTemplate, available: false }
            })

            this.templatePool = Object.values(tempTemplatePool).sort((a, b) => a.t.id - b.t.id)

            this.nodes = this.presets.slice()
            this.nodes.sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
        },
        // Utility func to translate from internal format to db
        convertToDB () {
            this.presets = this.nodes.slice()

            this.templates = []
            this.unusedTemplates = []

            this.templatePool.forEach((template) => {
                template.t.updated = template.updated
                if (template.available) {
                    this.templates.push(template.t)
                } else {
                    this.unusedTemplates.push(template.t)
                }
            })
        },
        startTour () {
            this.$intro().start()
        },
    },

    // Prompts user
    beforeRouteLeave (to, from, next) {
        if (this.isChanged && !window.confirm('Unsaved changes will be lost if you leave. Do you wish to continue?')) {
            next(false)
            return
        }

        next()
    },
}
</script>

<style lang="sass">
@import '~sass/partials/timeline-page-layout.sass'
</style>
