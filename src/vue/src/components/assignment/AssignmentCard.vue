<template>
    <b-card :class="$root.getBorderClass(assignment.id)">
        <slot class="float-right"/>
        <h2 class="d-inline">
            {{ assignment.name }}
        </h2><br/>
        <b-badge
            v-if="assignment.lti_couples > 0"
            v-b-tooltip.hover
            class="mt-2 info"
            title="Linked via LTI"
        >
            LTI
        </b-badge>
        <b-badge
            v-if="!assignment.is_published"
            v-b-tooltip.hover
            class="mt-2"
            title="Not visible to students:
            click to edit"
        >
            Unpublished
        </b-badge>
    </b-card>
</template>

<script>
export default {
    props: ['assignment'],
}
</script>
