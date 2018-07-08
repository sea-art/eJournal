<!--
    Card used in format editor to open template editor, toggle availability, delete templates from pool.
-->

<template>
    <b-card class="card no-hover" :class="color" style="">
        <b>{{ template.t.name }}</b>
        <icon @click.native.stop="emitDeleteTemplate" class="trash-icon ml-10 float-right" name="trash" scale="1.75"></icon>
        <toggle-switch @click.native.stop class="template-todo-card-switch" :isActive="isActive" @parentActive="template.available = $event"/>
    </b-card>
</template>

<script>
import Switch from '@/components/SwitchComponent.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['template', 'color'],
    data () {
        return {
            isActive: this.template.available
        }
    },
    methods: {
        emitDeleteTemplate () {
            if (confirm('Are you sure you wish to delete this template?')) {
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
</style>
