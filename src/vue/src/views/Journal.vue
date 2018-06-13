<template>
    <div>
        <b-row>
            <b-col cols="3" class="left-content">
                  <button v-on:click="variable = 0">Select entry 1</button>
                  <button v-on:click="variable = 1">Select entry 2</button>
            </b-col>
            <b-col cols="6" class="main-content">
                <h1>path enzo</h1>
                <!--
                    Fill in the template using the corresponding data
                    of the entry
                . -->
                <entry-template :textbox1="nodes[variable].textbox1"
                :textbox2="nodes[variable].textbox2"
                :deadline="nodes[variable].deadline">  </entry-template>
            </b-col>
            <b-col cols="3" class="right-content"></b-col>
        </b-row>
    </div>
</template>

<script>
import entryTemplate from '@/components/TemplateCard.vue'
export default {
    name: 'Journal',
    data () {
        return {
            variable: 0,
            nodes: [{
                textbox1: 'Awesome IT',
                textbox2: 'het was leuk veel dingen enzo.',
                deadline: '13-12-2018 23:00',
                id: '1'
            }, {
                textbox1: 'Lezing NNS',
                textbox2: 'Rob Belleman enzo',
                deadline: '14-03-2019 06:00',
                id: '2'
            }]
        }
    },
    components: {
        'entry-template': entryTemplate
    }
}
</script>
