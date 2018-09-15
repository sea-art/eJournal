<template>
    <b-card class="no-hover settings-card" :class="$root.getBorderClass($route.params.cID)">
        <h2>Assignment details</h2>
        <b-form @submit.prevent="onSubmit">
            <h2 class="field-heading">Assignment name</h2>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                     v-model="assignmentDetails.name"
                     placeholder="Assignment name"
                     @change="$emit('changed')"/>
            <h2 class="field-heading">Description</h2>
            <text-editor
                :id="'text-editor-assignment-edit-description'"
                :givenContent="assignmentDetails.description"
                @content-update="assignmentDetails.description = $event"
                @change="$emit('changed')"
                :footer="false"/>
            <h2 class="field-heading">Points possible</h2>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                v-model="assignmentDetails.points_possible"
                placeholder="Points"
                @change="$emit('changed')"
                type="number"/>
            <h2 class="field-heading">Unlock date</h2>
            <b-input
                class="mb-2 mr-sm-2 mb-sm-0 multi-form multi-date-input theme-input full-width"
                 :value="assignmentDetails.unlock_date && assignmentDetails.unlock_date.replace(' ', 'T')"
                 @input="assignmentDetails.unlock_date = $event && $event.replace('T', ' ')"
                 @change="$emit('changed')"
                 type="datetime-local"/>
            <h2 class="field-heading">Due date</h2>
            <b-input
                class="mb-2 mr-sm-2 mb-sm-0 multi-form multi-date-input theme-input full-width"
                :value="assignmentDetails.due_date && assignmentDetails.due_date.replace(' ', 'T')"
                @input="assignmentDetails.due_date = $event && $event.replace('T', ' ')"
                @change="$emit('changed')"
                type="datetime-local"/>
            <h2 class="field-heading">Lock date</h2>
            <b-input
                class="mb-2 mr-sm-2 mb-sm-0 multi-form multi-date-input theme-input full-width"
                :value="assignmentDetails.lock_date && assignmentDetails.lock_date.replace(' ', 'T')"
                @input="assignmentDetails.lock_date = $event && $event.replace('T', ' ')"
                @change="$emit('changed')"
                type="datetime-local"/>
        </b-form>
    </b-card>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'FormatEditAssignmentDetailsCard',
    props: {
        assignmentDetails: {
            required: true
        }
    },
    components: {
        'text-editor': textEditor,
        icon
    }
}
</script>
