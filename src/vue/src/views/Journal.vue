<template>
    <b-row no-gutters>
        <b-col v-if="bootstrapLg()" cols="12">
            <bread-crumb v-if="bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/>
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
        </b-col>
        <b-col v-else xl="3" class="left-content">
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
        </b-col>
        <b-col lg="12" xl="6" order="2" class="main-content">
            <bread-crumb v-if="!bootstrapLg()" @eye-click="customisePage" :currentPage="Placeholder" :course="Placeholder"/>
            <!--
                Fill in the template using the corresponding data
                of the entry
            . -->
            <div v-if="nodes[currentNode].type == 'entry'">
                <entry-template ref="entry-template-card" @edit-data="adaptData" :textbox1="nodes[currentNode].textbox1"
                    :textbox2="nodes[currentNode].textbox2"
                    :date="nodes[currentNode].date"></entry-template>
            </div>
            <div v-else-if="nodes[currentNode].type == 'add'">
                <add-card @add-template="addNode">bhjewk</add-card>
            </div>
            <div v-else-if="nodes[currentNode].type == 'progress'">
                <entry-template ref="entry-template-card" @edit-data="adaptData" :textbox1="nodes[currentNode].textbox1"
                    :textbox2="nodes[currentNode].textbox2"
                    :date="nodes[currentNode].date"></entry-template>
            </div>
        </b-col>
        <b-col cols="12" xl="3" order="3" class="right-content"/>
    </b-row>

</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import entryTemplate from '@/components/TemplateCard.vue'
import addCard from '@/components/AddCard.vue'
import edag from '@/components/Edag.vue'
import breadCrumb from '@/components/BreadCrumb.vue'

export default {
    name: 'Journal',
    props: {
        cID: {
            type: String,
            required: true
        },
        aID: {
            type: String,
            required: true
        },
        jID: {
            type: String,
            required: true
        }
    },
    data () {
        return {
            windowWidth: 0,
            currentNode: 0,
            editedData: ['', ''],
            nodes: [{
                type: 'entry',
                textbox1: 'Awesome IT',
                textbox2: 'Waar ging dit ook al weer over?',
                date: new Date(),
                id: 0
            }, {
                type: 'entry',
                textbox1: 'Lezing NNS',
                textbox2: 'Rob Belleman was er ook.',
                date: new Date(),
                id: 1
            }, {
                type: 'add',
                textbox1: 'Add',
                textbox2: 'something',
                text: '+',
                date: new Date(),
                id: 2
            }, {
                type: 'progress',
                textbox1: 'Jaar 1 Deadline',
                textbox2: 'oh no',
                text: '5',
                date: new Date(),
                id: 3
            }]
        }
    },

    methods: {
        adaptData (editedData) {
            this.nodes[this.currentNode].textbox1 = editedData[0]
            this.nodes[this.currentNode].textbox2 = editedData[1]
        },
        selectNode ($event) {
            if ($event === this.currentNode) {
                return this.currentNode
            }

            if (this.nodes[this.currentNode].type !== 'entry') {
                this.currentNode = $event
                return
            }

            if (this.$refs['entry-template-card'].saveEditMode === 'Save') {
                if (!confirm('Oh no! Progress will not be saved if you leave. Do you wish to continue?')) {
                    return
                }
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
        'entry-template': entryTemplate,
        'add-card': addCard,
        'edag': edag
    }
}
</script>

<style>
.noHoverCard:hover {
    background-color: var(--theme-light-grey);
}
</style>
