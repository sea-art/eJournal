<template>
    <div>
        <!-- Button used to check for different path for student and teacher  -->
        <button v-on:click="student = !student">with in assignment student {{student}}</button> <br>

        create assignment overview via database van de assignments <br>
        <router-link v-if="!student" tag="button" to="/Courses/PAV/Colloquium">Colloquium</router-link>
        <router-link v-if="student" tag="button" to="/Courses/PAV/Colloquium/Dennis">Colloquium</router-link>
    </div>
</template>

<script>
export default {
    name: 'assignmentOverview',
    data () {
        return {
            createNew: false,
            student: false
        }
    }
}
</script>
