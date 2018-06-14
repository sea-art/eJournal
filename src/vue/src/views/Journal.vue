<template>
    <div>
        <b-row>
            <b-col cols="3" class="left-content">
                  <edag @select-node="selectNode" :selected="variable" :nodes="nodes"></edag>
            </b-col>
            <b-col cols="6" class="main-content">
                <bread-crumb :currentPage="$route.params.student"></bread-crumb>
                <!--
                    Fill in the template using the corresponding data
                    of the entry
                . -->
                <entry-template ref="entry-template-card" @edit-data="adaptData" :textbox1="nodes[variable].textbox1"
                :textbox2="nodes[variable].textbox2"
                :date="nodes[variable].date">  </entry-template>
            </b-col>
            <b-col cols="3" class="right-content"></b-col>
        </b-row>
    </div>
</template>

<script>
import entryTemplate from '@/components/TemplateCard.vue'
import edag from '@/components/Edag.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
export default {
    name: 'Journal',
    data () {
        return {
            variable: 0,
            editedData: ['', ''],
            nodes: [{
                type: 'entry',
                textbox1: 'Awesome IT',
                textbox2: 'het was leuk veel dingen enzo.',
                date: new Date(),
                id: 0
            }, {
                type: 'entry',
                textbox1: 'Lezing NNS',
                textbox2: 'Rob Belleman enzo',
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
        selectNode ($event) {
            if ($event === this.variable) {
                return
            }
            if (this.$refs['entry-template-card'].save === 'Save') {
                if (!confirm('Oh no! Progress will not be saved if you leave. Do you wish to continue?')) {
                    return
                }
            }
            this.$refs['entry-template-card'].cancel()
            this.variable = $event
        },
        addNode ($event) {
            this.nodes.splice($event, 0, {
                type: 'entry',
                textbox1: '',
                textbox2: '',
                text: '',
                date: new Date(),
                id: this.node.length
            })
        }
    },

    components: {
        'bread-crumb': breadCrumb,
        'entry-template': entryTemplate,
        'edag': edag
    }
}
</script>
