<!--
    Used in a card in the format editor to open template editor, toggle availability, delete templates from pool.
-->

<template>
    <div
        class="template-link unselectable"
        @click="$emit('edit-template')"
    >
        <icon
            v-if="template.preset_only"
            v-b-tooltip.hover
            name="times"
            class="fill-red float-right ml-2"
            title="This template can only be used for preset entries you add to the timeline"
            @click.native.stop="togglePresetOnly"
        />
        <icon
            v-else
            v-b-tooltip.hover
            name="check"
            class="fill-green float-right ml-2"
            title="This template can be freely used by students as often as they want"
            @click.native.stop="togglePresetOnly"
        />
        <icon
            name="trash"
            class="trash-icon ml-2 float-right"
            @click.native.stop="emitDeleteTemplate"
        />
        <icon
            name="edit"
            class="edit-icon float-right"
        />
        <b
            v-if="template.name"
            class="max-one-line"
        >
            {{ template.name }}
        </b>
        <b
            v-else
            class="text-red"
        >
            Untitled template
        </b>
    </div>
</template>

<script>
export default {
    props: ['template'],
    methods: {
        emitDeleteTemplate () {
            if (window.confirm(
                `Are you sure you want to delete template "${this.template.name}" from this assignment?`)) {
                this.$emit('delete-template')
            }
        },
        togglePresetOnly () {
            this.template.preset_only = !this.template.preset_only
        },
    },
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.template-link
    padding: 5px
    border-style: solid
    border-color: $theme-dark-grey
    border-width: 1px 0px
    cursor: pointer
    vertical-align: middle
    svg
        margin-top: 3px
    .max-one-line
        width: calc(100% - 2em)
    .edit-icon
        margin-top: 4px
    .edit-icon, .trash-icon
        width: 0px
        visibility: hidden
    &:hover
        .max-one-line
            width: calc(100% - 5em)
        .edit-icon, .trash-icon
            visibility: visible
            width: auto
</style>
