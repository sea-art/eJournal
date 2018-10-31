<template>
    <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
        <h2>End of assignment</h2>
        <b v-if="assignment.lock_date && new Date(assignment.lock_date) < new Date()">This assignment has been locked.</b>
        <b v-else-if="student && assignment.due_date && new Date(assignment.due_date) < new Date()">The deadline for this assignment has passed.</b>
        <span v-else class="multi-form"> This is the end of the assignment.</span>
        <h2 class="field-heading" v-if="assignment.due_date">Due date</h2>
        <span v-if="assignment.due_date">{{ $root.beautifyDate(assignment.due_date) }}</span>
        <h2 class="field-heading" v-if="assignment.lock_date">Lock date</h2>
        <span v-if="assignment.lock_date">{{ $root.beautifyDate(assignment.lock_date) }}</span>
        <h2 class="field-heading" v-if="assignment.points_possible">Amount of points possible</h2>
        <span v-if="assignment.points_possible">{{ assignment.points_possible }}</span>
    </b-card>
</template>

<script>
export default {
    props: ['assignment', 'student']
}
</script>
