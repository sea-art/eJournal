<template>
    <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
        <h2>{{ assignment.name }}</h2>
        <div v-html="assignment.description"/>
        <h6 v-if="assignment.unlock_date">Unlock date</h6>
        <p v-if="assignment.unlock_date">{{ $root.beautifyDate(assignment.unlock_date) }}</p>
        <b v-if="student && assignment.due_date && new Date(assignment.due_date) < new Date()">The deadline for this assignment has passed.</b>
        <b v-if="assignment.unlock_date && new Date(assignment.unlock_date) > new Date()">This assignment is locked and will be made available later.</b>
    </b-card>
</template>

<script>
export default {
    props: ['assignment', 'student']
}
</script>
