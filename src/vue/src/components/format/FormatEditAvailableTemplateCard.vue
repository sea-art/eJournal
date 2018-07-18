<!--
    Card used in format editor to open template editor, toggle availability, delete templates from pool.
-->

<template>
    <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
        <b>{{ template.t.name }}</b>
        <b-button v-on:click.stop @click="emitDeleteTemplate" class="delete-button float-right">
            <icon name="trash"/>
            Delete
        </b-button>
        <toggle-switch @click.native.stop class="template-todo-card-switch" :isActive="isActive" @parentActive="template.available = $event"/>
    </b-card>
</template>

<script>
import Switch from '@/components/assets/SwitchComponent.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['template'],
    data () {
        return {
            isActive: this.template.available
        }
    },
    methods: {
        emitDeleteTemplate () {
            if (confirm('Are you sure you want to delete template "' + this.template + '" from this format?')) {
                this.$emit('delete-template', this.template)
            }
        }
    },
    components: {
        'icon': icon,
        'toggle-switch': Switch
    }
}
</script>

<style lang="sass">
.template-todo-card-switch
    float: right
    text-align: center
    margin-top: 2px
    margin-right: 5px
</style>
