<template>
    <b-row no-gutters>
        <!-- TODO: reopen bread-crumb when it is working again -->
        <b-col v-if="bootstrapLg()" cols="12">
            <!-- <bread-crumb v-if="bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/> -->
            <!-- <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/> -->
        </b-col>
        <b-col v-else xl="3" class="left-content">
            <!-- <edag @select-node="selectNode" :selected="currentNode" :nodes="presets"/> -->
        </b-col>

        <b-col lg="12" xl="6" order="2" class="main-content">
            <!-- <bread-crumb v-if="!bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/> -->
            <!--
                Fill in the template using the corresponding data
                of the entry
            . -->
            <div>
                <selected-node-card ref="entry-template-card" :templates="templatePool" @edit-data="presets[currentNode].template=$event"/>
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
            nodes: [],

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
            }],

            templatePool: []
        }
    },

    created () {
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
    },

    methods: {
        selectNode ($event) {
            if ($event === this.currentNode) {
                return
            }

            this.$refs['entry-template-card'].cancel()
            this.currentNode = $event
        },
        addNode () {
            this.nodes.splice(this.currentNode, 0, {
                type: 'entry',
                textbox1: '',
                textbox2: '',
                text: '',
                date: new Date(),
                id: this.nodes.length
            })
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
