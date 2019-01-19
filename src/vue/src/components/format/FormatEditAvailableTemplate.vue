<!--
    Card used in format editor to open template editor, toggle availability, delete templates from pool.
-->

<template>
    <div class="available-template">
        <icon
            name="trash"
            class="float-right trash-icon"
            @click.native="emitDeleteTemplate"
        />
        <icon
            name="edit"
            class="float-right edit-icon mr-2"
            @click.native="$emit('edit-template')"
        />
        <span
            @click="$emit('edit-template')">
            {{ template.t.name }}
        </span>
    </div>
</template>

<script>
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
            if (confirm('Are you sure you want to delete template "' + this.template.t.name + '" from this format?')) {
                this.$emit('delete-template', this.template)
            }
        }
    },
    components: {
        icon
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.available-template
    svg
        margin-top: 4px
    span
        font-weight: bold
        &:hover
            color: $theme-blue
            cursor: pointer
</style>
