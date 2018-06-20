<template>
    <content-columns>
        <b-form slot="main-content-column" @submit="onSubmit">
            <h1>{{pageName}}</h1>
            {{assignment}}

            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"
                     v-model="assignment.name"
                     placeholder="Assignment name"
                     required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"
                     type="date"
                     required/>
            <b-form-textarea class="descriptionTextArea"
                             :rows="3"
                             :max-rows="6"
                             v-model="assignment.description"
                             placeholder="Description"
                             required/>

            <b-button type="submit">Update Settings</b-button>
            <b-button :to="{name: 'Assignment', params: {cID: this.$route.params.cID, courseName: pageName}}">Back</b-button>
        <br/>
    </b-form>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import assignmentApi from '@/api/assignment.js'

export default {
    name: 'AssignmentEdit',
    data () {
        return {
            pageName: '',
            assignment: {},
            form: {}
        }
    },
    components: {
        'content-columns': contentColumns
    },
    created () {
        assignmentApi.get_assignemnt_data(this.$route.params.cID, this.$route.params.cID)
            .then(response => {
                this.assignment = response
                this.pageName = this.assignment.name
                // this.assignment.deadline = new date(this.assignment.deadline)
            })
            .catch(_ => alert('Error while loading assignment data'))
    },
    methods: {
        onSubmit (evt) {
            assignmentApi.update_assignment(this.$route.params.aID,
                this.assignment.name,
                this.assignment.description)
                .then(response => {
                    this.assignments = response
                    this.pageName = this.assignment.name
                })
        }
    }
}
</script>

<style>
</style>
