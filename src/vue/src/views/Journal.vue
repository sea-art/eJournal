<template>
    <div>
        <b-row>
            <b-col cols="3" class="left-content">
                  <edag @select-node="variable = $event" :selected="variable" :nodes="nodes"></edag>
            </b-col>
            <b-col cols="6" class="main-content">
                <h1>path enzo</h1>
                <!--
                    Fill in the template using the corresponding data
                    of the entry
                . -->
                <entry-template @edit-data="adaptData" :textbox1="nodes[variable].textbox1"
                :textbox2="nodes[variable].textbox2"
                :deadline="nodes[variable].deadline">  </entry-template>
            </b-col>
            <b-col cols="3" class="right-content"></b-col>
        </b-row>
    </div>
</template>

<script>
import entryTemplate from '@/components/TemplateCard.vue'
import edag from '@/components/Edag.vue'
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
                type: 'progress',
                textbox1: 'Jaar 1 Deadline',
                textbox2: 'oh no',
                text: '5',
                date: new Date(),
                id: 2
            }]
        }
    },

    methods: {
        adaptData (editedData) {
            this.nodes[this.variable].textbox1 = editedData[0],
            this.nodes[this.variable].textbox2 = editedData[1]
        }
    },

    components: {
        'entry-template': entryTemplate,
        'edag': edag
    }
}
</script>
