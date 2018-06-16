<template>
    <b-row no-gutters>
        {{ windowWidth }}
        <b-col lg="3" order="3" order-lg="1" class="left-content d-none d-lg-block">
            <edag @select-node="selectNode" :selected="variable" :nodes="nodes"></edag>
        </b-col>
        <b-col md="12" lg="6" order="2" class="main-content">
            <bread-crumb @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"></bread-crumb>
            <!--
                Fill in the template using the corresponding data
                of the entry
            . -->
            <div v-if="nodes[variable].type == 'entry'">
                <entry-template ref="entry-template-card" @edit-data="adaptData" :textbox1="nodes[variable].textbox1"
                    :textbox2="nodes[variable].textbox2"
                    :date="nodes[variable].date"></entry-template>
            </div>
            <div v-else-if="nodes[variable].type == 'add'">
                <add-card @add-template="addNode">bhjewk</add-card>
            </div>
            <div v-else-if="nodes[variable].type == 'progress'">
                <entry-template ref="entry-template-card" @edit-data="adaptData" :textbox1="nodes[variable].textbox1"
                    :textbox2="nodes[variable].textbox2"
                    :date="nodes[variable].date"></entry-template>
            </div>
        </b-col>
        <b-col md="12" lg="3" order="1" order-lg="3" class="right-content">
            <slot name="right-content-column"></slot>
        </b-col>
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
    data () {
        return {
            windowWidth: 0,
            variable: 0,
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
            this.nodes[this.variable].textbox1 = editedData[0]
            this.nodes[this.variable].textbox2 = editedData[1]
        },
        // TODO maak deze functies weer mooi en duidelijk
        selectNode ($event) {
            if (this.nodes[this.variable].type !== 'entry') {
                this.variable = $event
                return
            }

            if ($event === this.variable) {
                return
            }
            if (this.$refs['entry-template-card'].save && this.$refs['entry-template-card'].save === 'Save') {
                if (!confirm('Oh no! Progress will not be saved if you leave. Do you wish to continue?')) {
                    return
                }
            }
            this.$refs['entry-template-card'].cancel()
            this.variable = $event
        },
        addNode () {
            this.nodes.splice(this.variable, 0, {
                type: 'entry',
                textbox1: '',
                textbox2: '',
                text: '',
                date: new Date(),
                id: this.nodes.length
            })
        },
        getWindowWidth (event) {
            this.windowWidth = document.documentElement.clientWidth;
        },
        getWindowHeight (event) {
            this.windowHeight = document.documentElement.clientHeight;
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
        window.removeEventListener('resize', this.getWindowWidth);
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
