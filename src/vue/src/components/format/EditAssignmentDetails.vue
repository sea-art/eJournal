<template>
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
        </b-form>
    </b-card>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'

import store from '@/Store'
import icon from 'vue-awesome/components/Icon'
import assignmentAPI from '@/api/assignment'

export default {
    name: 'EditAssignmentDetails',
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
        assignmentAPI.get(this.aID, this.cID)
            .then(assignment => { this.assignment = assignment })
            .catch(error => { this.$toasted.error(error.response.data.description) })
    },
    methods: {
        onSubmit (evt) {
            assignmentAPI.update(this.aID, this.assignment)
                .then(assignment => {
                    this.assignment = assignment
                    this.$toasted.success('Updated assignment.')
                    store.clearCache()
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
    },
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb,
        'text-editor': textEditor,
        icon
    }
}
</script>
