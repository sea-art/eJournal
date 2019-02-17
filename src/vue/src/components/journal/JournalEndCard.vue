<template>
    <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
        <h2>End of assignment</h2>
        <b v-if="assignment.due_date && new Date(assignment.due_date) > new Date()">
            Due date: {{ $root.beautifyDate(assignment.due_date) }}<br/>
        </b>
        <b v-if="assignment.lock_date">
            <span v-if="new Date(assignment.lock_date) < new Date()">
                This assignment has been locked<br/>
            </span>
            Lock date: {{ $root.beautifyDate(assignment.lock_date) }}<br/>
        </b>
    </b-card>
</template>

<script>
export default {
    props: ['assignment', 'student']
}
</script>
