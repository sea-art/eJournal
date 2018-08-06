<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-card class="no-hover settings-card">
            <b-form @submit.prevent="onSubmit">
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                         v-model="assignment.name"
                         placeholder="Assignment name"
                         required/>
                <b-form-textarea class="multi-form theme-input"
                                 :rows="3"
                                 :max-rows="6"
                                 v-model="assignment.description"
                                 placeholder="Description"
                                 required/>
                <b-button v-if="$root.canDeleteAssignment()" @click.prevent.stop="deleteAssignment()" class="delete-button multi-form float-left">
                    <icon name="trash"/>
                    Delete Assignment
                </b-button>
                <b-button
                    v-if="$root.canEditAssignment()"
                    class="change-button multi-form float-left"
                    :to="{ name: 'FormatEdit', params: { cID: cID, aID: aID } }">
                    <icon name="edit"/>
                    Edit Assignment Format
                </b-button>
                <b-button type="submit" class="add-button float-right">
                    <icon name="save"/>
                    Save
                </b-button>
            </b-form>
        </b-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import store from '@/Store'
import icon from 'vue-awesome/components/Icon'
import auth from '@/api/auth'

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
        auth.get('assignments/' + this.aID)
            .then(response => {
                this.assignment = response
                this.pageName = this.assignment.name
            })
    },
    methods: {
        onSubmit (evt) {
            auth.update('assignments/' + this.aID, this.assignment)
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
        'bread-crumb': breadCrumb,
        'icon': icon
    }
}
</script>
