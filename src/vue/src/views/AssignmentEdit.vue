<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-card class="no-hover">
            <b-form @submit.prevent="onSubmit">
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

                <b-button type="submit" class="change-button">Update Assignment</b-button>
                <b-button @click.prevent.stop="deleteAssignment()" class="delete-button">Delete Assignment</b-button>
            </b-form>
        </b-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import assignmentApi from '@/api/assignment.js'
import store from '@/Store'

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
    created () {
        assignmentApi.get_assignment_data(this.cID, this.aID)
            .then(response => {
                this.assignment = response
                this.pageName = this.assignment.name
            })
    },
    methods: {
        onSubmit (evt) {
            assignmentApi.update_assignment(this.aID,
                this.assignment.name,
                this.assignment.description)
                .then(response => {
                    this.assignments = response
                    this.pageName = this.assignment.name
                    this.$toasted.success('Updated assignment')
                    store.clearCache()
                    this.$router.push({
                        name: 'Assignment',
                        params: {
                            cID: this.cID,
                            aID: this.aID
                        }
                    })
                })
        },
        deleteAssignment () {
            if (confirm('Are you sure you want to delete ' + this.assignment.name + '?')) {
                assignmentApi.delete_assignment(this.cID, this.aID)
                    .then(response => {
                        this.$router.push({name: 'Course',
                            params: {
                                cID: this.cID,
                                courseName: this.$route.params.courseName
                            }})
                        this.$toasted.success('Deleted assignment')
                    })
            }
        }
    },
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb
    }
}
</script>

<style>
.descriptionTextArea {
    margin-bottom: 10px;
}
</style>
