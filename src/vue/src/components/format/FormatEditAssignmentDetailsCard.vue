<template>
    <b-card class="no-hover settings-card" :class="$root.getBorderClass($route.params.cID)">
        <pretty-checkbox
            class="p-svg float-right mt-1"
            color="primary"
            id="publishCheckbox"
            @change="updatePublishTooltip"
            v-model="assignmentDetails.is_published"
            v-b-tooltip.hover="assignmentDetails.is_published ? 'Visible to students' : 'Invisible to students'"
            toggle>
            <svg slot="extra" class="svg svg-icon" viewBox="0 0 20 20">
                <path d="M7.629,14.566c0.125,0.125,0.291,0.188,0.456,0.188c0.164,0,0.329-0.062,0.456-0.188l8.219-8.221c0.252-0.252,0.252-0.659,0-0.911c-0.252-0.252-0.659-0.252-0.911,0l-7.764,7.763L4.152,9.267c-0.252-0.251-0.66-0.251-0.911,0c-0.252,0.252-0.252,0.66,0,0.911L7.629,14.566z"
                      style="stroke: white;fill:white">
                </path>
            </svg>
                <b>Published</b>
            <label slot="off-label">Unpublished</label>
        </pretty-checkbox>

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
            <h2 class="field-heading">Points possible</h2>
            <b-input class="multi-form theme-input"
                v-model="assignmentDetails.points_possible"
                placeholder="Points"
                type="number"/>
            <b-row>
                <b-col xl="4">
                    <h2 class="field-heading">Unlock date</h2>
                    <flat-pickr class="multi-form theme-input full-width"
                    v-model="assignmentDetails.unlock_date"
                    :config="$root.flatPickrTimeConfig"/>
                </b-col>
                <b-col xl="4">
                    <h2 class="field-heading">Due date</h2>
                    <flat-pickr class="multi-form theme-input full-width"
                    v-model="assignmentDetails.due_date"
                    :config="$root.flatPickrTimeConfig"/>
                </b-col>
                <b-col xl="4">
                    <h2 class="field-heading">Lock date</h2>
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
import icon from 'vue-awesome/components/Icon'
import prettyCheckbox from 'pretty-checkbox-vue/check'

export default {
    name: 'FormatEditAssignmentDetailsCard',
    props: {
        assignmentDetails: {
            required: true
        }
    },
    components: {
        'text-editor': textEditor,
        'pretty-checkbox': prettyCheckbox,
        icon
    },
    data () {
        return {
            prevDate: ''
        }
    },
    methods: {
        updatePublishTooltip () {
            /* Ensures correct value of is_publish is set through v-model and the title bind can update.
             * Still has issues with fast cursor movement triggering focus inbetween. */
            this.$nextTick(() => {
                this.$root.$emit('bv::hide::tooltip', 'publishCheckboxTooltip')
                this.$root.$emit('bv::show::tooltip', 'publishCheckboxTooltip')
            })
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

<style lang="scss">
$pretty--color-primary: #252C39;
@import 'pretty-checkbox/src/pretty-checkbox.scss';
</style>
