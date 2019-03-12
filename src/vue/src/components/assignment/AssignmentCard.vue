<template>
    <b-card :class="$root.getBorderClass(assignment.id)">
        <slot class="float-right"></slot>
        <h2 class="d-inline">{{ assignment.name }}</h2><br/>
        <b-badge
            v-if="assignment.lti_couples > 0"
            class="mt-2 info"
            v-b-tooltip.hover
            title="Linked via LTI">
            LTI
        </b-badge>
        <b-badge
            v-if="!assignment.is_published"
            class="mt-2"
            v-b-tooltip.hover
            title="Not visible to students:
            click to edit">
            Unpublished
        </b-badge>
    </b-card>
</template>

<script>
export default {
    props: ['assignment']
}
</script>
