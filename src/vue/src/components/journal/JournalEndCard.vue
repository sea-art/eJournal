<template>
    <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
        <h2>End of assignment</h2>
        <p>This is the end of the assignment.</p>
        <h6 v-if="assignment.due_date">Due date</h6>
        <p v-if="assignment.due_date">{{ $root.beautifyDate(assignment.due_date) }}</p>
        <h6 v-if="assignment.points_possible">Amount of points possible</h6>
        <p v-if="assignment.points_possible">{{ assignment.points_possible }}</p>
        <h6 v-if="assignment.lock_date">Lock date</h6>
        <p v-if="assignment.lock_date">{{ $root.beautifyDate(assignment.lock_date) }}</p>
        <b v-if="student && assignment.due_date && new Date(assignment.due_date) < new Date()">The deadline for this assignment has passed.</b>
        <b v-if="assignment.lock_date && new Date(assignment.lock_date) < new Date()">This assignment has been locked.</b>
    </b-card>
</template>

<script>
export default {
    props: ['assignment', 'student']
}
</script>
