<!--
    Mini component representing the circle for a node in the EDAG.
    Handles its own style depending on a state given by parent.
-->

<template>
    <div class="edag-node-circle d-flex align-items-center justify-content-center" :class="classObject">
        <div v-if="this.entrystate === 'empty'" class="edag-node-circle-inner" :class="classObject"></div>
        <icon v-else-if="this.entrystate != ''" :name="iconName" class="edag-node-circle-icon fill-white" :scale="iconScale"></icon>
        <div v-else class="text-white">{{ text }}</div>
    </div>
</template>

<script>
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['type', 'text', 'selected', 'entrystate'],
    computed: {
        classObject () {
            return {
                'enc-entry': this.type === 'e',
                'enc-deadline': this.type === 'd',
                'enc-progress': this.type === 'p',
                'enc-add': this.type === 'a',
                'enc-selected': this.selected
            }
        },
        iconName () {
            switch (this.entrystate) {
            case 'grading':
                return 'hourglass-half'
            case 'graded':
                return 'check'
            case 'fulfilled':
                return 'check'
            case 'failed':
                return 'times'
            case 'needsgrading':
                return 'exclamation'
            case 'addNode':
                return 'plus'
            default:
                return ''
            }
        },
        iconScale () {
            if (this.entrystate === 'addNode') {
                if (this.selected) {
                    return '2'
                } else {
                    return '1'
                }
            }
            if (this.selected) {
                return '2.5'
            } else {
                return '1.5'
            }
        }
    },
    components: {
        'icon': icon
    }
}
</script>

<style>
.text-white {
    color: white;
}

.fill-white {
    fill: white;
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

.edag-node-circle-inner {
    width: 2em;
    height: 2em;
    background-color: white;
    border-radius: 50% !important;
    border-style: solid;
    border-width: 5px;
    border-color: white;
}

.edag-node-circle-inner.enc-selected {
    width: 3em;
    height: 3em;
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
