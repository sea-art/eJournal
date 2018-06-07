<template>
    <div>
        <h1>{{ msg }}</h1>
        <button v-on:click="student = !student">student {{student}}</button> <br>
        Hello {{ $route.params.course }} <br>
        <overview v-if="!createNew || student"></overview>
        <newAssign v-if="createNew && !student"></newAssign>
        <button v-if="!student" v-on:click="newToggle">{{ButtonCreateNew}}</button>
    </div>
</template>

<script>
import overview from '@/components/assignmentOverview'
import newAssign from '@/components/newAssign'
export default {
    name: 'courses',
    components: {
        overview,
        newAssign
    },
    data () {
        return {
            createNew: false,
            student: false,
            ButtonCreateNew: 'new assignment'
        }
    },
    methods: {
        newToggle () {
            this.createNew = !this.createNew
            if (this.createNew) {
                this.ButtonCreateNew = 'Cancel'
            } else {
                this.ButtonCreateNew = 'new assignment'
            }
        }
    }
}
</script>
