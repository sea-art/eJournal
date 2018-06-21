<template>
    <content-columns>
        <b-form slot="main-content-column" @submit="onSubmit">
            <h1>{{pageName}}</h1>

            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"
                     v-model="assignment.name"
                     placeholder="Assignment name"
                     required/>
            <b-form-textarea class="descriptionTextArea"
                             :rows="3"
                             :max-rows="6"
                             v-model="assignment.description"
                             placeholder="Description"
                             required/>

            <b-button type="submit">Update Assignment</b-button>
            <b-button @click.prevent.stop="deleteAssignment()">Delete Assignment</b-button>
            <b-button :to="{name: 'Assignment', params: {cID: cID, courseName: pageName}}">Back</b-button>
        <br/>
    </b-form>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import assignmentApi from '@/api/assignment.js'

export default {
    name: 'AssignmentEdit',
    props: {
        cID: {
            required: true
        },
        aID: {
            required: true
        }
    },
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
        assignmentApi.get_assignment_data(this.cID, this.aID)
            .then(response => {
                this.assignment = response
                this.pageName = this.assignment.name
            })
            .catch(_ => alert('Error while loading assignment data'))
    },
    methods: {
        onSubmit (evt) {
            assignmentApi.update_assignment(this.aID,
                this.assignment.name,
                this.assignment.description)
                .then(response => {
                    this.assignments = response
                    this.pageName = this.assignment.name
                })
        },
        deleteAssignment () {
            if (confirm('Are you sure you want to delete ' + this.assignment.name + '?')) {
                assignmentApi.delete_assignment(this.aID)
                    .then(response => {
                        this.$router.push({name: 'Course',
                            params: {
                                cID: this.cID,
                                courseName: this.$route.params.courseName
                            }})
                    })
            }
        }
    }
}
</script>

<style>
.descriptionTextArea {
    margin-bottom: 10px;
}
</style>
