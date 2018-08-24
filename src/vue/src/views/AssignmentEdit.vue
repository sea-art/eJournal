<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-card class="no-hover settings-card">
            <b-form @submit.prevent="onSubmit">
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                         v-model="assignment.name"
                         placeholder="Assignment name"
                         required/>
                <text-editor
                    :id="'text-editor-assignment-edit-description'"
                    :givenContent="assignment.description"
                    @content-update="assignment.description = $event"
                    :footer="false"
                    class="multi-form"
                 />
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
import textEditor from '@/components/assets/TextEditor.vue'
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
            assignment: {},
            form: {}
        }
    },
    created () {
        auth.get('assignments/' + this.aID)
            .then(assignment => {
                this.assignment = assignment
            })
            .catch(error => { this.$toasted.error(error.response.data.description) })
    },
    methods: {
        onSubmit (evt) {
            auth.update('assignments/' + this.aID, this.assignment)
                .then(assignment => {
                    this.assignment = assignment
                    this.$toasted.success('Updated assignment.')
                    store.clearCache()
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        deleteAssignment () {
            if (confirm('Are you sure you want to delete ' + this.assignment.name + '?')) {
                auth.delete('assignments/' + this.aID, { cID: this.cID })
                    .then(_ => {
                        this.$router.push({name: 'Course',
                            params: {
                                cID: this.cID,
                                courseName: this.$route.params.courseName
                            }})
                        this.$toasted.success('Deleted assignment.')
                    })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        }
    },
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb,
        'text-editor': textEditor,
        icon
    }
}
</script>
