<template>
    <content-columns>
        <edag slot="left-content-column" @select-node="selectNode" :selected="variable" :nodes="nodes"></edag>
        <div slot="main-content-column">
            <bread-crumb :currentPage="$route.params.assignmentName" :course="$route.params.courseName"></bread-crumb>
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
        </div>
    </content-columns>
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
        selectNode ($event) {
            if ($event === this.variable) {
                return
            }

            if (this.nodes[this.variable].type !== 'entry') {
                this.variable = $event
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
        addNode () {
            this.nodes.splice(this.variable, 0, {
                type: 'entry',
                textbox1: '',
                textbox2: '',
                text: '',
                date: new Date(),
                id: this.nodes.length
            })
        }
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
