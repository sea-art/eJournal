<!--
    Mini component representing the circle for a node in the EDAG.
    Handles its own style depending on a state given by parent.
-->

<template>
    <div class="edag-node-circle d-flex align-items-center justify-content-center text-white" :class="classObject" v-html="this.text">
    </div>
</template>

<script>
export default {
    props: ['type', 'text', 'selected'],
    computed: {
        classObject () {
            return {
                'enc-entry': this.type === 'e',
                'enc-deadline': this.type === 'd',
                'enc-progress': this.type === 'p',
                'enc-add': this.type === 'a',
                'enc-selected': this.selected
            }
        }
    }
}
</script>

<style>
.text-white {
    color: white;
}

.edag-node-circle {
    width: 4em;
    height: 4em;
    border-radius: 50% !important;
    border-style: solid;
    border-width: 5px;
    border-color: white;
}

.edag-node-circle.enc-selected {
    width: 5em;
    height: 5em;
}

.edag-node-circle.enc-add {
    width: 3em;
    height: 3em;
}

.edag-node-circle.enc-selected.enc-add {
    width: 4em;
    height: 4em;
}

.edag-node-circle.enc-entry {
    background-color: var(--theme-medium-grey)
}

.edag-node-circle.enc-entry:hover {
    background-color: var(--theme-dark-grey)
}

.edag-node-circle.enc-entry.enc-selected {
    background-color: var(--theme-dark-grey)
}

.edag-node-circle.enc-deadline {
    background-color: var(--theme-peach)
}

.edag-node-circle.enc-deadline:hover {
    background-color: var(--theme-dark-peach)
}

.edag-node-circle.enc-deadline.enc-selected {
    background-color: var(--theme-dark-peach)
}

.edag-node-circle.enc-progress {
    background-color: var(--theme-pink)
}

.edag-node-circle.enc-progress:hover {
    background-color: var(--theme-red)
}

.edag-node-circle.enc-progress.enc-selected {
    background-color: var(--theme-red)
}

.edag-node-circle.enc-add {
    background-color: var(--theme-blue)
}

.edag-node-circle.enc-add:hover {
    background-color: var(--theme-dark-blue)
}

.edag-node-circle.enc-add.enc-selected {
    background-color: var(--theme-dark-blue)
}
</style>
