<template>
    <b-card class="no-hover" :class="this.accomplished ? 'red-border' : 'green-border'">
        <h2 class="mb-2">Goal: {{ currentNode.target }} points</h2>
        <span v-if="!this.accomplished">
            <b>{{ score }}</b> out of <b>{{ currentNode.target }}</b> points.<br/>
            <b>{{ Math.round(left * 1000) / 1000 }}</b> more required before <b>{{ $root.beautifyDate(currentNode.deadline) }}</b>.<br/>
        </span>
        <p>{{ currentNode.description }}</p>
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
            return this.score > this.currentNode.target
        },
        left () {
            return this.currentNode.target - this.score
        }
    }
}
</script>
