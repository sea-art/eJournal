<template>
    <div>
        <b-row>
            <b-col cols="3" class="left-content">
                  <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"></edag>
            </b-col>
            <b-col cols="6" class="main-content">
                <bread-crumb :currentPage="$route.params.student"></bread-crumb>
                <!--
                    Fill in the template using the corresponding data
                    of the entry
                . -->
                <div v-if="nodes[currentNode].type == 'entry'">
                  <entry-template @edit-data="adaptData" :textbox1="nodes[currentNode].textbox1"
                  :textbox2="nodes[currentNode].textbox2"
                  :date="nodes[currentNode].date">  </entry-template>
                </div>
                <div v-else-if="nodes[currentNode].type == 'add'">
                    <add-card @add-template="addNode">bhjewk</add-card>
                </div>
                <div v-else-if="nodes[currentNode].type == 'progress'">
                  <entry-template @edit-data="adaptData" :textbox1="nodes[currentNode].textbox1"
                  :textbox2="nodes[currentNode].textbox2"
                  :date="nodes[currentNode].date">  </entry-template>
                </div>
            </b-col>
            <b-col cols="3" class="right-content"></b-col>
        </b-row>
    </div>
</template>

<script>
import entryTemplate from '@/components/TemplateCard.vue'
import addCard from '@/components/AddCard.vue'
import edag from '@/components/Edag.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
export default {
    name: 'Journal',
    data () {
        return {
            currentNode: 0,
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
            this.nodes[this.currentNode].textbox1 = editedData[0]
            this.nodes[this.currentNode].textbox2 = editedData[1]
        },
        // TODO maak deze functies weer mooi en duidelijk
        selectNode ($event) {
            if (this.nodes[this.currentNode].type !== 'entry') {
                this.currentNode = $event
                return
            }

            if ($event === this.currentNode) {
                return
            }
            if (this.$refs['entry-template-card'].save && this.$refs['entry-template-card'].save === 'Save') {
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
        }
    },

    components: {
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
