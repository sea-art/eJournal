<template>
    <div>
        <!--
        <h1>{{ msg }}</h1>

        Button used to check for different path for student and teacher
        <button v-on:click="student = !student">student {{student}}</button> <br>

        Hello {{ $route.params.course }} <br>

        <overview v-if="!createNew || student"></overview>
        <newAssign v-if="createNew && !student"></newAssign>
        Toggle between the 2 components above
        <button v-if="!student" v-on:click="newToggle">{{ButtonCreateNew}}</button>
    -->
    </div>
</template>

<script>
/* imports the components so they can be used as tags in the html */
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
            names: ['Webprogrammeren en databases project',
                    'Academische vaardigheden informatica 2',
                    'Academische vaardigheden informatica 1'],
            authors: ['Robert van Wijk',
                      'Robert van Wijk',
                      'Robert van Wijk'],
            startdates: ['01-01-2017',
                         '01-01-2017',
                         '01-01-2017']
        }
    }
    // data () {
    //     return {
    //         createNew: false,
    //         student: false,
    //         ButtonCreateNew: 'new assignment'
    //     }
    // },
    // methods: {
    //     newToggle () {
    //         this.createNew = !this.createNew
    //         if (this.createNew) {
    //             this.ButtonCreateNew = 'Cancel'
    //         } else {
    //             this.ButtonCreateNew = 'new assignment'
    //         }
    //     }
    // }
}
</script>
