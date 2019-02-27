<template>
    <b-card class="no-hover settings-card" :class="$root.getBorderClass($route.params.cID)">
        <div class="d-flex float-right multi-form">
            <b-button v-if="assignmentDetails.is_published" @click="assignmentDetails.is_published = false" class="add-button flex-grow-1" v-b-tooltip.hover title="This assignment is visible to students">
                <icon name="check"/>
                Published
            </b-button>
            <b-button v-if="!assignmentDetails.is_published" @click="assignmentDetails.is_published = true" class="delete-button flex-grow-1" v-b-tooltip.hover title="This assignment is not visible to students">
                <icon name="times"/>
                Unpublished
            </b-button>
        </div>

        <h2>Assignment details</h2>
        <b-form @submit.prevent="onSubmit">
            <h2 class="field-heading">Assignment name</h2>
            <b-input class="multi-form theme-input"
                     v-model="assignmentDetails.name"
                     placeholder="Assignment name"/>
            <h2 class="field-heading">Description</h2>
            <text-editor class="multi-form"
                :id="'text-editor-assignment-edit-description'"
                :givenContent="assignmentDetails.description"
                @content-update="assignmentDetails.description = $event"
                :footer="false"/>
            <h2 class="field-heading">
                Points possible
                <tooltip tip="The amount of points that represents a perfect score for this assignment, excluding bonus points"/>
            </h2>
            <b-input class="multi-form theme-input"
                v-model="assignmentDetails.points_possible"
                placeholder="Points"
                type="number"/>
            <b-row>
                <b-col xl="4">
                    <h2 class="field-heading">
                        Unlock date
                        <tooltip tip="Students will be able to work on the assignment from this date onwards"/>
                    </h2>
                    <flat-pickr class="multi-form theme-input full-width"
                        v-model="assignmentDetails.unlock_date"
                        :config="$root.flatPickrTimeConfig"/>
                </b-col>
                <b-col xl="4">
                    <h2 class="field-heading">
                        Due date
                        <tooltip tip="Students are expected to have finished their assignment by this date, but new entries can still be added until the lock date"/>
                    </h2>
                    <flat-pickr class="multi-form theme-input full-width"
                        v-model="assignmentDetails.due_date"
                        :config="$root.flatPickrTimeConfig"/>
                </b-col>
                <b-col xl="4">
                    <h2 class="field-heading">
                        Lock date
                        <tooltip tip="No more entries can be added after this date" />
                    </h2>
                    <flat-pickr class="multi-form theme-input full-width"
                        v-model="assignmentDetails.lock_date"
                        :config="$root.flatPickrTimeConfig"/>
                </b-col>
            </b-row>
        </b-form>
    </b-card>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'
import tooltip from '@/components/assets/Tooltip.vue'
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
        'tooltip': tooltip,
        icon
    },
    data () {
        return {
            prevDate: ''
        }
    },
    watch: {
        assignmentDetails: {
            handler: function (newAssignmentDetails) {
                var patt = new RegExp('T')

                /*  When the date is loaded in from the db this format
                    will be adapted to the flatpickr format,
                    which triggers this watcher.
                    These changes happen in the initial load and when it's
                    saved. This will be ignored as an unsaved change by the
                    following regex if-statement.  */
                if (!patt.test(newAssignmentDetails.lock_date) && !patt.test(this.prevDate)) {
                    this.$emit('changed')
                }

                this.prevDate = newAssignmentDetails.lock_date
            },
            deep: true
        }
    }
}
</script>
