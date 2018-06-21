<!-- TODO: add loading and saving apis, add links to template editor, add navigation guards to cache format on template edit and to confirm navigation away when unsaved, add client side checks for improper formats upon saving -->

<template>
    <b-row no-gutters>
        <!-- TODO: reopen bread-crumb when it is working again -->
        <b-col v-if="bootstrapLg()" cols="12">
            <!-- <bread-crumb v-if="bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/> -->
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
        </b-col>
        <b-col v-else xl="3" class="left-content">
            <b-button @click.prevent.stop="addNode"> Add Preset </b-button>
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
        </b-col>

        <b-col lg="12" xl="6" order="2" class="main-content">
            <!-- <bread-crumb v-if="!bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/> -->
            <!--
                Fill in the template using the corresponding data
                of the entry
            . -->
            <b-button @click.prevent.stop="saveFormat"> Save </b-button>

            <div>
                <selected-node-card ref="entry-template-card" :currentPreset="nodes[currentNode]" :templates="templatePool" @edit-data="nodes[currentNode].template=$event"/>
            </div>
        </b-col>
        <b-col cols="12" xl="3" order="3" class="right-content">
            <h3>Template Pool</h3>
            <template-todo-card v-for="template in templatePool" :template="template" :key="template.t.tID" :color="'pink-border'"/>
            <b-card class="card hover" :class="'grey-border'" style="">
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

export default {
    name: 'FormatEdit',

    props: ['cID', 'aID'],

    data () {
        return {
            windowWidth: 0,
            currentNode: 0,

            templates: [{
                'tID': 1,
                'name': 'Template 2',
                'fields': [{ 'title': 'Field 1', 'eID': '0' }]
            }, {
                'tID': 0,
                'name': 'Template 1',
                'fields': [{ 'title': 'Field 1', 'eID': '0' }, { 'title': 'Field 2', 'eID': '1' }]
            }],

            presets: [{
                'type': 'd',
                'deadline': 'some string',
                'template': {
                    'tID': 0,
                    'name': 'Template 1',
                    'fields': [{ 'title': 'Field 1', 'eID': '0' }, { 'title': 'Field 2', 'eID': '1' }]
                }
            }, {
                'type': 'd',
                'deadline': 'some string',
                'template': {
                    'tID': 2,
                    'name': 'Template 3',
                    'fields': [{ 'title': 'Field 1', 'eID': '0' }, { 'title': 'Field 2', 'eID': '1' }]
                }
            }, {
                'type': 'p',
                'deadline': 'some string',
                'target': 5
            }],

            templatePool: [],
            nodes: []
        }
    },

    created () {
        this.convertFromDB()
    },

    methods: {
        selectNode ($event) {
            if ($event === this.currentNode) {
                return
            }

            this.currentNode = $event
        },
        addNode () {
            this.nodes.push({
                'type': 'd',
                'deadline': '',
                'template': (this.templatePool) ? this.templatePool[0].t : null
            })
        },
        // Do client side validation and save to DB
        saveFormat () {
            var invalidDate = false
            var invalidTemplate = false
            var invalidTarget = false

            var templatePoolts = []
            for (var template of this.templatePool) {
                templatePoolts.push(template.t)
            }
            for (var node of this.nodes) {
                if (!invalidDate && isNaN(Date.parse(node.deadline))) {
                    invalidDate = true
                    alert('One or more presets has an invalid deadline. Please check the format and try again.')
                }
                if (!invalidTemplate && node.type === 'd' && !templatePoolts.includes(node.template)) {
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

            for (var template of this.templates) {
                idInPool.push(template.tID)
                this.templatePool.push({ t: template, a: true })
            }
            for (var preset of this.presets) {
                if (preset.type === 'd' && !idInPool.includes(preset.template.tID)) {
                    idInPool.push(preset.template.tID)
                    this.templatePool.push({ t: preset.template, a: false })
                }
            }

            this.templatePool.sort((a, b) => { return a.t.tID - b.t.tID })

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
        'selected-node-card': formatEditSelectTemplateCard
    }
}
</script>

<style>
.noHoverCard:hover {
    background-color: var(--theme-light-grey);
}
</style>
