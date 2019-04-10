<template>
    <b-card class="no-hover" :class="borderColor">
        <h2 class="mb-2">Target: {{ currentNode.target }} point<span v-if="currentNode.target > 1">s</span></h2>
        <p v-if="currentNode.description" class="mb-0">{{ currentNode.description }}</p>
        <hr class="full-width"/>
        <span v-if="!this.accomplished && new Date() < new Date(this.currentNode.due_date)">
            <b>{{ score }}</b> out of <b>{{ currentNode.target }}</b> points.<br/>
            <b>{{ Math.round(left * 1000) / 1000 }}</b> more required before <b>{{ $root.beautifyDate(currentNode.due_date) }}</b>.<br/>
        </span>
        <b v-else-if="!this.accomplished">Not achieved.</b>
        <b v-else>Successfully achieved.</b>
    </b-card>
</template>

<script>
export default {
    props: ['nodes', 'currentNode'],
    computed: {
        score () {
            /* The function will update a given progressNode by
            * going through all the nodes and count the published grades
            * so far. */
            var tempProgress = 0
            for (var node of this.nodes) {
                if (node.nID === this.currentNode.nID) {
                    break
                }

                if (node.type === 'e' || node.type === 'd') {
                    if (node.entry && node.entry.grade && node.entry.published && node.entry.grade !== '0') {
                        tempProgress += parseFloat(node.entry.grade)
                    }
                }
            }
            return tempProgress
        },
        accomplished () {
            return this.score >= this.currentNode.target
        },
        left () {
            return this.currentNode.target - this.score
        },
        borderColor () {
            return {
                'green-border': this.accomplished,
                'red-border': !this.accomplished && new Date() > new Date(this.currentNode.due_date),
                'orange-border': !this.accomplished && new Date() < new Date(this.currentNode.due_date)
            }
        }
    }
}
</script>
