<template>
    <b-row class="outer-container" no-gutters>
        <b-col md="12" lg="8" xl="9" class="inner-container-edag-page">
            <b-col md="12" lg="auto" xl="4" class="left-content-edag-page">
                <bread-crumb v-if="$root.lgMax()" class="main-content">&nbsp;</bread-crumb>
                <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
            </b-col>

            <b-col md="12" lg="auto" xl="8" class="main-content-edag-page">
                <bread-crumb v-if="$root.xl()" class="main-content">&nbsp;</bread-crumb>
                <div v-if="nodes.length > currentNode">
                    <div v-if="nodes[currentNode].type == 'e'">
                        <entry-node
                            ref="entry-template-card"
                            @edit-node="adaptData"
                            :cID="cID"
                            :entryNode="nodes[currentNode]"/>
                    </div>
                    <div v-else-if="nodes[currentNode].type == 'd'">
                        <div v-if="nodes[currentNode].entry !== null">
                            <entry-node :cID="cID" ref="entry-template-card" @edit-node="adaptData" :entryNode="nodes[currentNode]"/>
                        </div>
                        <div v-else>
                            <div v-if="checkDeadline()">
                                <entry-preview ref="entry-template-card" @content-template="fillDeadline" :template="nodes[currentNode].template"/>
                            </div>
                            <div v-else>
                                The deadline has passed, you can't make another submission
                            </div>
                        </div>
                    </div>
                    <div v-else-if="nodes[currentNode].type == 'a'">
                        <add-card @info-entry="addNode" :addNode="nodes[currentNode]"/>
                    </div>
                    <div v-else-if="nodes[currentNode].type == 'p'">
                        <b-card class="no-hover" :class="'pink-border'">
                            <h2 class="mb-2">Needed progress</h2>
                            You have {{progressNodes[nodes[currentNode].nID]}} points out of the {{nodes[currentNode].target}}
                            needed points before {{nodes[currentNode].deadline}}.
                        </b-card>
                    </div>
                </div>
            </b-col>
        </b-col>

        <b-col md="12" lg="4" xl="3" class="right-content-journal right-content">
            <h3>Assignment Description</h3>
            <b-card class="no-hover">
                {{ assignmentDescription }}
            </b-card>
        </b-col>
    </b-row>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import entryNode from '@/components/entry/EntryNode.vue'
import addCard from '@/components/journal/AddCard.vue'
import edag from '@/components/edag/Edag.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import journal from '@/api/journal'
import entryPreview from '@/components/entry/EntryPreview.vue'
import assignmentApi from '@/api/assignment.js'

export default {
    props: ['cID', 'aID', 'jID'],
    data () {
        return {
            currentNode: 0,
            editedData: ['', ''],
            nodes: [],
            progressNodes: {},
            assignmentDescription: ''
        }
    },
    created () {
        journal.get_nodes(this.jID)
            .then(response => {
                this.nodes = response.nodes
                if (this.$route.query.nID !== undefined) {
                    this.currentNode = this.findEntryNode(parseInt(this.$route.query.nID))
                }

                for (var node of this.nodes) {
                    if (node.type === 'p') {
                        this.progressPoints(node)
                    }
                }
            })
            .catch(_ => this.$toasted.error('Error while loading nodes.'))

        assignmentApi.get_assignment_data(this.cID, this.aID)
            .then(response => {
                this.assignmentDescription = response.description
            })
            .catch(_ => this.$toasted.error('Error while loading assignment description.'))
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
            journal.create_entry(this.jID, this.nodes[this.currentNode].entry.template.tID, editedData.entry.content, this.nodes[this.currentNode].nID)
                .then(response => {
                    this.nodes = response.nodes
                    this.currentNode = response.added
                })
        },
        selectNode ($event) {
            /* Function that prevents you from instant leaving an EntryNode
             * or a DeadlineNode when clicking on a different node in the
             * tree. */
            if ($event === this.currentNode) {
                return this.currentNode
            }

            if (this.nodes[this.currentNode].type !== 'e' || this.nodes[this.currentNode].type !== 'd') {
                this.currentNode = $event
                return
            }

            if (this.$refs['entry-template-card'].saveEditMode === 'Save') {
                if (!confirm('Progress will not be saved if you leave. Do you wish to continue?')) {
                    return
                }
            }

            this.$refs['entry-template-card'].cancel()
            this.currentNode = $event
        },
        addNode (infoEntry) {
            journal.create_entry(this.jID, infoEntry[0].tID, infoEntry[1])
                .then(response => {
                    this.nodes = response.nodes
                    this.currentNode = response.added
                })
        },
        fillDeadline (data) {
            journal.create_entry(this.jID, this.nodes[this.currentNode].template.tID, data, this.nodes[this.currentNode].nID)
                .then(response => {
                    this.nodes = response.nodes
                    this.currentNode = response.added
                })
        },
        progressPoints (progressNode) {
            /* The function will update a given progressNode by
             * going through all the nodes and count the published grades
             * so far. */
            var tempProgress = 0
            for (var node of this.nodes) {
                if (node.nID === progressNode.nID) {
                    break
                }

                if (node.type === 'e' || node.type === 'd') {
                    if (node.entry && node.entry.grade && node.entry.grade !== '0') {
                        tempProgress += parseInt(node.entry.grade)
                    }
                }
            }

            this.progressNodes[progressNode.nID] = tempProgress
        },
        findEntryNode (nodeID) {
            for (var i = 0; i < this.nodes.length; i++) {
                if (this.nodes[i].nID === nodeID) {
                    return i
                }
            }
            return 0
        },
        checkDeadline () {
            var currentDate = new Date()
            var deadline = new Date(this.nodes[this.currentNode].deadline)

            return currentDate <= deadline
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'add-card': addCard,
        'edag': edag,
        'entry-node': entryNode,
        'entry-preview': entryPreview
    }
}
</script>
