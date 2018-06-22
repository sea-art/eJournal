<!-- TODO: add loading and saving apis, add links to template editor-->

<template>
    <b-row no-gutters>
        <!-- TODO: reopen bread-crumb when it is working again -->
        <b-col v-if="bootstrapLg()" cols="12">
            <!-- <bread-crumb v-if="bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/> -->
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodesSorted"/>
        </b-col>
        <b-col v-else xl="3" class="left-content">
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodesSorted"/>
        </b-col>

        <b-col lg="12" xl="6" order="2" class="main-content">
            <!-- <bread-crumb v-if="!bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/> -->
            <!--
                Fill in the template using the corresponding data
                of the entry
            . -->

            <div v-if="nodes.length > 0">
                <selected-node-card ref="entry-template-card" :currentPreset="nodesSorted[currentNode]" :templates="templatePool"/>
            </div>
            <div v-else>
                <p>No presets yet</p>
            </div>

            <b-modal
                ref="modal"
                title="test"
                hide-footer
                hide-header
                @hidden="hideModal">
                    <template-editor :template="templateBeingEdited"></template-editor>
            </b-modal>
        </b-col>
        <b-col cols="12" xl="3" order="3" class="right-content">
            <h3>Format</h3>
            <b-card @click.prevent.stop="addNode" class="card hover" :class="'grey-border'" style="">
                <b>Add Preset</b>
            </b-card>
            <b-card @click.prevent.stop="saveFormat" class="card hover" :class="'grey-border'" style="">
                <b>Save Format</b>
            </b-card>
            <br/>

            <h3>Template Pool</h3>
            <template-todo-card v-for="template in templatePool" :key="template.t.tID" @click.native="showModal(template.t)" :template="template" :color="'pink-border'"/>
            <b-link :to="{ name: 'TemplateEdit', params: { aID: aID, tID: 1 } }">
                <b-card class="card hover" :class="'grey-border'" style="">
                    <b>+ Add Template</b>
                </b-card>
            </b-link>
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
import store from '@/Store.vue'
import templateEdit from '@/components/TemplateEdit.vue'

export default {
    name: 'FormatEdit',

    props: ['cID', 'aID', 'editedTemplate'],

    data () {
        return {
            windowWidth: 0,
            currentNode: 0,

            templates: [],
            presets: [],

            templatePool: [],
            nodes: [],
            templateMap: {},

            isChanged: false,

            templateBeingEdited: {
                'type': 'd',
                'deadline': this.newDate(),
                'template': (this.templatePool) ? this.templatePool[0].t : null
            },
            templatesEdited: []
        }
    },

    computed: {
        nodesSorted () {
            // return this.nodes.sort((a, b) => { return new Date(a.deadline) - new Date(b.deadline) })
            return this.nodes
        }
    },

    created () {

    },

    watch: {
        templatePool: {
            handler: function () { this.isChanged = true }
        },
        nodes: {
            handler: function () { this.isChanged = true }
        }
    },

    methods: {
        showModal (template) {
            this.templateBeingEdited = template
            this.$refs['modal'].show()
        },
        hideModal () {
            this.templatesEdited.push(this.templateBeingEdited)
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
                'template': (this.templatePool) ? this.templatePool[0].t : null
            })
        },
        // Do client side validation and save to DB
        saveFormat () {
            var invalidDate = false
            var invalidTemplate = false
            var invalidTarget = false

            var templatePoolIds = []
            for (var template of this.templatePool) {
                templatePoolIds.push(template.t.tID)
            }
            for (var node of this.nodes) {
                if (!invalidDate && isNaN(Date.parse(node.deadline))) {
                    invalidDate = true
                    alert('One or more presets has an invalid deadline. Please check the format and try again.')
                }
                if (!invalidTemplate && node.type === 'd' && !templatePoolIds.includes(node.template.tID)) {
                    invalidTemplate = true
                    alert('One or more presets has an invalid template. Please check the format and try again.')
                }
                if (!invalidTarget && node.type === 'p' && isNaN(parseInt(node.target))) {
                    invalidTarget = true
                    alert('One or more presets has an invalid target. Please check the format and try again.')
                }
            }

            if (invalidDate | invalidTemplate | invalidTarget) {
                return
            }

            this.convertToDB()

            for (var editedTemplate of this.templatesEdited) {
                // journalAPI.update_template().then(data => { editedTemplate.tID = data.tID })
            }

            journalAPI.update_format(this.aID, this.templates, this.presets)
        },
        getWindowWidth (event) {
            this.windowWidth = document.documentElement.clientWidth
        },
        getWindowHeight (event) {
            this.windowHeight = document.documentElement.clientHeight
        },
        bootstrapLg () {
            return this.windowHeight < 1200
        },
        bootstrapMd () {
            return this.windowHeight < 922
        },
        customisePage () {
            alert('Wishlist: Customise page')
        },
        // Utility func to translate from db format to internal
        convertFromDB () {
            var idInPool = []
            var tempTemplatePool = []

            for (var template of this.templates) {
                idInPool.push(template.tID)
                tempTemplatePool.push({ t: template, a: true })
            }
            for (var preset of this.presets) {
                if (preset.type === 'd' && !idInPool.includes(preset.template.tID)) {
                    idInPool.push(preset.template.tID)
                    tempTemplatePool.push({ t: preset.template, a: false })
                }
            }

            tempTemplatePool.sort((a, b) => { return a.t.tID - b.t.tID })

            this.templatePool = tempTemplatePool

            this.nodes = this.presets.slice()
        },
        // Utility func to translate from internal format to db
        convertToDB () {
            this.presets = this.nodes.slice()

            this.templates = []

            for (var template of this.templatePool) {
                if (template.a) {
                    this.templates.push(template.t)
                }
            }
        }
    },

    mounted () {
        this.$nextTick(function () {
            window.addEventListener('resize', this.getWindowWidth)

            this.getWindowWidth()
        })
    },
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

    beforeRouteEnter (to, from, next) {
        if (from.name === 'TemplateEdit') {
            next(vm => {
                vm.templatePool = store.state.format.templatePool
                vm.nodes = store.state.format.nodes
            })
        } else {
            next(vm => {
                journalAPI.get_format(vm.aID).then(data => { vm.templates = data.format.templates; vm.presets = data.format.presets; vm.convertFromDB(); vm.isChanged = false })
            })
        }
        next()
    },

    beforeRouteLeave (to, from, next) {
        if (to.name === 'TemplateEdit') {
            store.setFormat(this.templatePool, this.nodes)
        } else {
            if (this.isChanged && !confirm('Oh no! Unsaved changes will be lost if you leave. Do you wish to continue?')) {
                next(false)
                return
            } else {
                store.clearFormat()
            }
        }

        next()
    }
}
</script>

<style>
.noHoverCard:hover {
    background-color: var(--theme-light-grey);
}
</style>
