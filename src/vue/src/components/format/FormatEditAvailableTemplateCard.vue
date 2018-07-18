<!--
    Card used in format editor to open template editor, toggle availability, delete templates from pool.
-->

<template>
    <b-card :class="$root.getBorderClass($route.params.cID)">
        <!-- <toggle-switch @click.native.stop class="template-todo-card-switch" :isActive="isActive" @parentActive="template.available = $event"/> -->
        <div class="float-right">
            <b-button v-on:click.stop v-if="!template.available" @click="toggleActive" class="delete-button full-width">
                <icon name="times"/>
                Disabled
            </b-button>
            <b-button v-on:click.stop v-if="template.available" @click="toggleActive" class="add-button full-width">
                <icon name="check"/>
                Enabled
            </b-button><br>
            <b-button v-on:click.stop @click="emitDeleteTemplate" class="delete-button button-top-border full-width">
                <icon name="trash"/>
                Delete
            </b-button>
        </div>
        <span>
            <icon name="edit" class="edit-template-icon"/>
            <b clas>{{ template.t.name }}</b>
        </span>
    </b-card>
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
            if (confirm('Are you sure you want to delete template "' + this.template + '" from this format?')) {
                this.$emit('delete-template', this.template)
            }
        },
        toggleActive () {
            this.template.available = !this.template.available
        }
    },
    components: {
        'icon': icon
    }
}
</script>

<style lang="sass">
.edit-template-icon
    position: relative
    top: 2px
</style>
