<template>
    <b-row no-gutters>
        <!-- TODO: reopen bread-crumb when it is working again -->
        <b-col v-if="bootstrapLg()" cols="12">
            <!-- <bread-crumb v-if="bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/> -->
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
        </b-col>
        <b-col v-else xl="3" class="left-content">
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
        </b-col>

        <b-col lg="12" xl="6" order="2" class="main-content">
            <!-- <bread-crumb v-if="!bootstrapLg()" @eye-click="customisePage" :currentPage="$route.params.assignmentName" :course="$route.params.courseName"/> -->
            <div v-if="nodes.length > currentNode">
                <div v-if="nodes[currentNode].type == 'e'">
                    <entry-node ref="entry-template-card" @edit-node="adaptData" :entryNode="nodes[currentNode]"/>
                </div>
                <div v-else-if="nodes[currentNode].type == 'd'">
                    {{nodes[currentNode]}}
                    <entry-node ref="entry-template-card" @edit-node="adaptData" :entryNode="nodes[currentNode]"/>
                </div>
                <div v-else-if="nodes[currentNode].type == 'a'">
                    <add-card @info-entry="addNode" :addNode="nodes[currentNode]"></add-card>
                </div>
                <div v-else-if="nodes[currentNode].type == 'p'">
                    <b-card class="card main-card noHoverCard" :class="'pink-border'">
                        <h2>Needed progress</h2>
                        You have {{progressNodes[nodes[currentNode].nID]}} points out of the {{nodes[currentNode].target}}
                        needed points before {{nodes[currentNode].deadline}}.
                    </b-card>
                </div>
            </div>
        </b-col>
        <b-col cols="12" xl="3" order="3" class="right-content"/>
    </b-row>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import entryNode from '@/components/EntryNode.vue'
import addCard from '@/components/AddCard.vue'
import edag from '@/components/Edag.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import journal from '@/api/journal'

export default {
    props: ['cID', 'aID', 'jID'],
    data () {
        return {
            currentNode: 0,
            editedData: ['', ''],
            nodes: [],
            progressNodes: {}
        }
    },
    created () {
        journal.get_nodes(this.jID)
            .then(response => { this.nodes = response.nodes })
            .catch(_ => alert('Error while loading nodes.'))
    },
    watch: {
        currentNode: function () {
            if (this.nodes[this.currentNode].type === 'p') {
                this.progressPoints(this.nodes[this.currentNode])
            }
        }
    },
    methods: {
        adaptData (editedData) {
            this.nodes[this.currentNode] = editedData
        },
        selectNode ($event) {
            if ($event === this.currentNode) {
                return this.currentNode
            }

            if (this.nodes[this.currentNode].type !== 'e' || this.nodes[this.currentNode].type !== 'd') {
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
        addNode (infoEntry) {
            journal.create_entry(this.jID, infoEntry[0].tID, infoEntry[1])
            journal.get_nodes(this.jID)
                .then(response => { this.nodes = response.nodes })
                .catch(_ => alert('Error while loading nodes.'))
        },
        progressPoints (progressNode) {
            var tempProgress = 0

            for (var node of this.nodes) {
                if (node.nID === progressNode.nID) {
                    break
                }

                if (node.type === 'e' || node.type === 'd') {
                    tempProgress += node.entry.grade
                }
            }

            this.progressNodes[progressNode.nID] = tempProgress
        },
        bootstrapLg () {
            return this.windowHeight < 1200
        },
        bootstrapMd () {
            return this.windowHeight < 922
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'add-card': addCard,
        'edag': edag,
        'entry-node': entryNode
    }
}
</script>
