<template>
    <content-columns>
        <b-form slot="main-content-column" @submit="onSubmit">
            <h1>{{pageName}}</h1>
            <!-- <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="assignment.name" placeholder="Assignment name" required/> -->
            <!-- <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="assignment.deadline" type="date" required/> -->
            <!-- <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="assignment.description" placeholder="Description" required/> -->
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
            })
            .catch(_ => alert('Error while loading assignemnt data'))
    },
    methods: {
        onSubmit (evt) {
        }
    }
}
</script>
