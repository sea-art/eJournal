<!--
    Edag component. Handles the prop connection with parent, as well as any
    functionality involving the list (ie. showing the list,
    passing selected state)

    Example data:
    data () {
        return {
            selected: 2,
            nodes: [
                {
                    type: 'entry',
                    text: '',
                    id: 0,
                    date: new Date()
                },
                {
                    type: 'entry',
                    text: '',
                    id: 1,
                    date: new Date()
                },
                {
                    type: 'entry',
                    text: '',
                    id: 2,
                    date: new Date()
                },
                {
                    type: 'progress',
                    text: '5',
                    id: 3,
                    date: new Date()
                }
            ]
        }
    }
-->

<template>
    <div class="scrollbar-parent-div">
        <div id="edag-div" class="scrollbar-child-div" ref="scd" :style="styleObject">
            <edag-node v-for="node in this.nodes" @select-node="$emit('select-node', $event)" :node="node" :selected="isSelected(node.id)" :key="node.id"/>
        </div>
    </div>
</template>

<script>
import edagNode from '@/components/EdagNode'

export default {
    props: ['selected', 'nodes'],
    data () {
        return {
            padright: 0
        }
    },
    methods: {
        isSelected (id) {
            return id === this.selected
        }
    },
    computed: {
        styleObject () {
            return {
                'padding-right': this.padright + 'px'
            }
        }
    },
    components: {
        'edag-node': edagNode
    },
    mounted () {
        this.padright = this.$refs.scd.offsetWidth - this.$refs.scd.clientWidth
    }
}
</script>

<style>
#edag-div {
}

.scrollbar-parent-div {
    height: 100%;
    width: 100%;
    overflow: hidden;
}

.scrollbar-child-div {
    width: 100%;
    height: 99%;
    overflow: auto;
    overflow-x: hidden;
    padding-right: 0px; /* exact value is given in JavaScript code */
    box-sizing: content-box;
}
</style>
