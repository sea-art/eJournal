<template>
    <b-row
        class="outer-container-timeline-page"
        noGutters
    >
        <b-col
            md="12"
            lg="8"
            xl="9"
            class="inner-container-timeline-page"
        >
            <b-col
                md="12"
                lg="auto"
                xl="4"
                class="left-content-timeline-page"
            >
                <bread-crumb v-if="$root.lgMax"/>
                <timeline
                    :selected="currentNode"
                    :nodes="nodes"
                    @select-node="selectNode"
                />
            </b-col>

            <b-col
                md="12"
                lg="auto"
                xl="8"
                class="main-content-timeline-page"
            >
                <bread-crumb v-if="$root.xl"/>
                <div v-if="nodes.length > currentNode && currentNode !== -1">
                    <div v-if="nodes[currentNode].type == 'e'">
                        <entry-node
                            ref="entry-template-card"
                            :journal="journal"
                            :cID="cID"
                            :entryNode="nodes[currentNode]"
                            @edit-node="adaptData"
                            @delete-node="deleteNode"
                        />
                    </div>
                    <div v-else-if="nodes[currentNode].type == 'd'">
                        <div v-if="nodes[currentNode].entry !== null">
                            <entry-node
                                ref="entry-template-card"
                                :cID="cID"
                                :entryNode="nodes[currentNode]"
                                @edit-node="adaptData"
                                @delete-node="deleteNode"
                            />
                        </div>
                        <div v-else>
                            <entry-preview
                                v-if="!isLocked()"
                                ref="entry-prev"
                                :template="nodes[currentNode].template"
                                :nodeID="nodes[currentNode].nID"
                                :description="nodes[currentNode].description"
                                @content-template="fillDeadline"
                            />
                            <b-card
                                v-else
                                :class="$root.getBorderClass($route.params.cID)"
                                class="no-hover"
                            >
                                <h2 class="mb-2">
                                    {{ nodes[currentNode].template.name }}
                                </h2>
                                <hr class="full-width"/>
                                <b>This preset is locked. You cannot submit an entry at the moment.</b><br/>
                                {{ deadlineRange }}
                            </b-card>
                        </div>
                    </div>
                    <div v-else-if="nodes[currentNode].type == 'a'">
                        <add-card
                            ref="add-card-ref"
                            :addNode="nodes[currentNode]"
                            @info-entry="addNode"
                        />
                    </div>
                    <div v-else-if="nodes[currentNode].type == 'p'">
                        <progress-node
                            :currentNode="nodes[currentNode]"
                            :nodes="nodes"
                        />
                    </div>
                </div>
                <journal-start-card
                    v-else-if="currentNode === -1"
                    :assignment="assignment"
                />
                <journal-end-card
                    v-else
                    :assignment="assignment"
                    :student="true"
                />
            </b-col>
        </b-col>

        <b-col
            md="12"
            lg="4"
            xl="3"
            class="right-content-timeline-page right-content"
        >
            <h3>Journal progress</h3>
            <b-card
                :class="$root.getBorderClass($route.params.cID)"
                class="no-hover"
            >
                <progress-bar
                    v-if="journal.stats"
                    :currentPoints="journal.stats.acquired_points"
                    :totalPoints="journal.stats.total_points"
                    :bonusPoints="journal.bonus_points"
                    :comparePoints="assignment.stats ? assignment.stats.average_points : -1"
                />
            </b-card>

            <transition name="fade">
                <b-button
                    v-if="$root.lgMax && addIndex > -1 && currentNode !== addIndex"
                    class="fab"
                    @click="currentNode = addIndex"
                >
                    <icon
                        name="plus"
                        scale="1.5"
                    />
                </b-button>
            </transition>
            <b-card
                :class="$root.getBorderClass($route.params.cID)"
                class="no-hover"
            >
                <h2>Journal members</h2>
                <ul class="member-list">
                    <li
                        v-for="student in journal.students"
                        :key="student.id"
                    >
                        {{ student.full_name }}
                    </li>
                </ul>
                <b-button
                    class="mr-1 flex-grow-1 delete-button"
                    tag="b-button"
                    @click="leaveJournal()"
                >
                    <icon name="sign-out"/>
                    Leave group
                </b-button>
            </b-card>
        </b-col>
    </b-row>
</template>
<style lang="sass">
.member-list
    padding: 0
    margin-bottom: 0
    li
        list-style-type: none
        line-height: 2.5em
        padding-bottom: 0px
        margin-bottom: 0px
        border-bottom: 1px solid #eee
    li:last-child
        border-bottom: none

</style>

<script>
import entryNode from '@/components/entry/EntryNode.vue'
import entryPreview from '@/components/entry/EntryPreview.vue'
import addCard from '@/components/journal/AddCard.vue'
import timeline from '@/components/timeline/Timeline.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import progressBar from '@/components/assets/ProgressBar.vue'
import journalStartCard from '@/components/journal/JournalStartCard.vue'
import journalEndCard from '@/components/journal/JournalEndCard.vue'
import progressNode from '@/components/entry/ProgressNode.vue'

import journalAPI from '@/api/journal.js'
import assignmentAPI from '@/api/assignment.js'
import entryAPI from '@/api/entry.js'

export default {
    components: {
        breadCrumb,
        addCard,
        timeline,
        entryNode,
        entryPreview,
        progressBar,
        progressNode,
        journalStartCard,
        journalEndCard,
    },
    props: ['cID', 'aID', 'jID'],
    data () {
        return {
            currentNode: -1,
            editedData: ['', ''],
            nodes: [],
            journal: {},
            assignment: '',
        }
    },
    computed: {
        addIndex () {
            return this.nodes.findIndex(node => node.type === 'a')
        },
        deadlineRange () {
            const unlockDate = this.$root.beautifyDate(this.nodes[this.currentNode].unlock_date)
            const lockDate = this.$root.beautifyDate(this.nodes[this.currentNode].lock_date)

            if (unlockDate && lockDate) {
                return `Available from ${unlockDate} until ${lockDate}`
            } else if (unlockDate) {
                return `Available from ${unlockDate}`
            } else if (lockDate) {
                return `Available until ${lockDate}`
            }

            return ''
        },
    },
    watch: {
        currentNode () {
            if (this.currentNode !== -1
                && this.currentNode !== this.nodes.length
                && this.nodes[this.currentNode].type === 'p') {
                this.progressPoints(this.nodes[this.currentNode])
                this.progressPointsLeft = this.nodes[this.currentNode].target
                    - this.progressNodes[this.nodes[this.currentNode].nID]
            }
        },
    },
    created () {
        assignmentAPI.get(this.aID, this.cID, { customErrorToast: 'Error while loading assignment data.' })
            .then((assignment) => {
                this.assignment = assignment

                if ((!this.assignment.unlock_date || new Date(this.assignment.unlock_date) < new Date())
                    && (!this.assignment.lock_date || new Date(this.assignment.lock_date) > new Date())) {
                    journalAPI.getNodes(this.jID)
                        .then((nodes) => {
                            this.nodes = nodes
                            if (this.$route.query.nID !== undefined) {
                                this.currentNode = this.findEntryNode(parseInt(this.$route.query.nID, 10))
                            }
                        })
                }
            })

        journalAPI.get(this.jID)
            .then((journal) => { this.journal = journal })
    },
    methods: {
        leaveJournal () {
            if (window.confirm('Are you sure you want to leave this journal?')) {
                journalAPI.leave(this.jID)
                    .then(() => {
                        this.$router.push({
                            name: 'CreateJoinJournal',
                            params: {
                                cID: this.cID, aID: this.aID,
                            },
                        })
                    })
            }
        },
        adaptData (editedData) {
            this.nodes[this.currentNode] = editedData
            entryAPI.update(this.nodes[this.currentNode].entry.id, { content: editedData.entry.content })
                .then((entry) => { this.nodes[this.currentNode].entry = entry })
        },
        deleteNode () {
            entryAPI.delete(this.nodes[this.currentNode].entry.id, { responseSuccessToast: true })
                .then(() => {
                    if (this.nodes[this.currentNode].type === 'd') {
                        this.nodes[this.currentNode].entry = null
                        this.currentNode = 0
                    } else {
                        this.nodes.splice(this.currentNode, 1)
                    }
                })
        },
        discardChanges () {
            /*  Checks the node and depending of the type of node
             *  it will look for possible unsaved changes.
             *  If there are unsaved changes a confirmation will be asked.
             */
            if (this.currentNode !== -1
                && this.currentNode !== this.nodes.length
                && this.nodes[this.currentNode].type === 'd'
                && this.nodes[this.currentNode].entry === null
                && !this.isLocked()) {
                if (this.$refs['entry-prev'].checkChanges()
                    && !window.confirm('Progress will not be saved if you leave. Do you wish to continue?')) {
                    return false
                }
            }

            if (this.currentNode !== -1
                && this.currentNode !== this.nodes.length
                && this.nodes[this.currentNode].type === 'd'
                && this.nodes[this.currentNode].entry !== null) {
                if (this.$refs['entry-template-card'].saveEditMode === 'Save'
                    && !window.confirm('Progress will not be saved if you leave. Do you wish to continue?')) {
                    return false
                }
            }

            if (this.currentNode !== -1
                && this.currentNode !== this.nodes.length
                && this.nodes[this.currentNode].type === 'a') {
                if (this.$refs['add-card-ref'].checkChanges()
                    && !window.confirm('Progress will not be saved if you leave. Do you wish to continue?')) {
                    return false
                }
            }

            if (this.currentNode !== -1
                && this.currentNode !== this.nodes.length
                && this.nodes[this.currentNode].type === 'e') {
                if (this.$refs['entry-template-card'].saveEditMode === 'Save'
                    && !window.confirm('Progress will not be saved if you leave. Do you wish to continue?')) {
                    return false
                }
            }

            return true
        },
        selectNode ($event) {
            /* Function that prevents you from instant leaving an EntryNode
             * or a DeadlineNode when clicking on a different node in the
             * timeline. */
            if ($event === this.currentNode) {
                return this.currentNode
            }

            if (this.discardChanges()) {
                this.currentNode = $event
            }

            return undefined
        },
        addNode (infoEntry) {
            entryAPI.create({
                journal_id: this.jID,
                template_id: infoEntry[0].id,
                content: infoEntry[1],
            })
                .then((data) => {
                    this.nodes = data.nodes
                    this.currentNode = data.added
                })
        },
        fillDeadline (data) {
            entryAPI.create({
                journal_id: this.jID,
                template_id: this.nodes[this.currentNode].template.id,
                content: data,
                node_id: this.nodes[this.currentNode].nID,
            })
                .then((localData) => {
                    this.nodes = localData.nodes
                    this.currentNode = localData.added
                })
        },
        findEntryNode (nodeID) {
            for (let i = 0; i < this.nodes.length; i++) {
                if (this.nodes[i].nID === nodeID) {
                    return i
                }
            }
            return 0
        },
        isLocked () {
            const currentDate = new Date()
            let unlockDate = currentDate
            let lockDate = currentDate

            if (this.nodes[this.currentNode].unlock_date) {
                unlockDate = new Date(this.nodes[this.currentNode].unlock_date)
            }

            if (this.nodes[this.currentNode].lock_date) {
                lockDate = new Date(this.nodes[this.currentNode].lock_date)
            }

            return currentDate < unlockDate || lockDate < currentDate
        },
    },
}
</script>
