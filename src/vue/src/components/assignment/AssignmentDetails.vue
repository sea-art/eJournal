<template>
    <b-form
        @submit.prevent="onSubmit"
        @reset.prevent="onReset"
    >
        <h2 class="field-heading required">
            Assignment name
        </h2>
        <b-input
            v-model="assignmentDetails.name"
            class="multi-form theme-input"
            placeholder="Assignment name"
            required
        />
        <h2 class="field-heading">
            Description
        </h2>
        <text-editor
            id="text-editor-assignment-edit-description"
            v-model="assignmentDetails.description"
            :footer="false"
            class="multi-form"
            placeholder="Description of the assignment"
        />
        <h2 class="field-heading required">
            Points possible
            <tooltip
                tip="The amount of points that represents a perfect score for this assignment, excluding
                bonus points"
            />
        </h2>
        <b-input
            v-model="assignmentDetails.points_possible"
            class="multi-form theme-input"
            placeholder="Points"
            type="number"
            min="0"
            required
        />
        <b-row class="multi-form">
            <b-col xl="4">
                <h2 class="field-heading">
                    Unlock date
                    <tooltip tip="Students will be able to work on the assignment from this date onwards"/>
                </h2>
                <flat-pickr
                    v-model="assignmentDetails.unlock_date"
                    :config="Object.assign({}, {
                        maxDate: assignmentDetails.dueDate ? assignmentDetails.dueDate : assignmentDetails.lockDate
                    }, $root.flatPickrTimeConfig)"
                />
            </b-col>
            <b-col xl="4">
                <h2 class="field-heading">
                    Due date
                    <tooltip
                        tip="Students are expected to have finished their assignment by this date, but new entries
                        can still be added until the lock date"
                    />
                </h2>
                <flat-pickr
                    v-model="assignmentDetails.due_date"
                    :config="Object.assign({}, {
                        minDate: assignmentDetails.unlockDate,
                        maxDate: assignmentDetails.lockDate,
                    }, $root.flatPickrTimeConfig)"
                />
            </b-col>
            <b-col xl="4">
                <h2 class="field-heading">
                    Lock date
                    <tooltip tip="No more entries can be added after this date"/>
                </h2>
                <flat-pickr
                    v-model="assignmentDetails.lock_date"
                    :config="Object.assign({}, {
                        minDate: assignmentDetails.dueDate ? assignmentDetails.dueDate : assignmentDetails.unlockDate
                    }, $root.flatPickrTimeConfig)"
                />
            </b-col>
        </b-row>
        <h2 class="field-heading">
            Options
        </h2>
        <div>
            <b-button
                v-if="assignmentDetails.is_published"
                v-b-tooltip.hover
                class="add-button mr-2 multi-form"
                title="This assignment is visible to students.
                Once an assignment is published, it cannot be unpublished"
                @click="assignmentDetails.is_published = false"
            >
                <icon name="check"/>
                Published
            </b-button>
            <b-button
                v-if="!assignmentDetails.is_published"
                v-b-tooltip.hover
                class="delete-button mr-2 multi-form"
                title="This assignment is not visible to students.
                Once an assignment is published, it cannot be unpublished"
                @click="assignmentDetails.is_published = true"
            >
                <icon name="times"/>
                Unpublished
            </b-button>

            <br/>

            <b-button
                v-if="assignmentDetails.is_group_assignment"
                v-b-tooltip.hover
                class="change-button mr-2 multi-form"
                title="This assignment is made in groups"
                @click="assignmentDetails.is_group_assignment = false"
            >
                <icon name="users"/>
                Group assignment
            </b-button>
            <b-button
                v-if="!assignmentDetails.is_group_assignment"
                v-b-tooltip.hover
                class="change-button mr-2 multi-form"
                title="This assignment is made in individually"
                @click="assignmentDetails.is_group_assignment = true"
            >
                <icon name="user"/>
                Individual assignment
            </b-button>

            <b-button
                v-if="assignmentDetails.is_group_assignment && assignmentDetails.can_lock_journal"
                v-b-tooltip.hover
                class="add-button mr-2 multi-form"
                title="Students are allowd to lock the journal they are in. Once locked, no other students can join."
                @click="assignmentDetails.can_lock_journal = false"
            >
                <icon name="check"/>
                Journal can be locked
            </b-button>
            <b-button
                v-if="assignmentDetails.is_group_assignment && !assignmentDetails.can_lock_journal"
                v-b-tooltip.hover
                class="delete-button mr-2 multi-form"
                title="Students are not allowd to lock the journal they are in.
                       Once locked, no other students can join."
                @click="assignmentDetails.can_lock_journal = true"
            >
                <icon name="times"/>
                Journal cannot be locked
            </b-button>

            <br/>

            <b-button
                v-if="assignmentDetails.can_set_journal_name"
                v-b-tooltip.hover
                class="add-button mr-2 multi-form"
                title="Students are allowed to change the journal name"
                @click="assignmentDetails.can_set_journal_name = false"
            >
                <icon name="check"/>
                Custom journal names
            </b-button>
            <b-button
                v-if="!assignmentDetails.can_set_journal_name"
                v-b-tooltip.hover
                class="delete-button mr-2 multi-form"
                title="Students are not allowed to change the journal name"
                @click="assignmentDetails.can_set_journal_name = true"
            >
                <icon name="times"/>
                Custom journal names
            </b-button>

            <b-button
                v-if="assignmentDetails.can_set_journal_image"
                v-b-tooltip.hover
                class="add-button mr-2 multi-form"
                title="Students are allowed to change the journal image"
                @click="assignmentDetails.can_set_journal_image = false"
            >
                <icon name="check"/>
                Custom journal images
            </b-button>
            <b-button
                v-if="!assignmentDetails.can_set_journal_image"
                v-b-tooltip.hover
                class="delete-button mr-2 multi-form"
                title="Students are not allowed to change the journal image"
                @click="assignmentDetails.can_set_journal_image = true"
            >
                <icon name="times"/>
                Custom journal images
            </b-button>
        </div>
    </b-form>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'
import tooltip from '@/components/assets/Tooltip.vue'

export default {
    name: 'AssignmentDetails',
    components: {
        textEditor,
        tooltip,
    },
    props: {
        assignmentDetails: {
            required: true,
        },
        isNew: {
            default: false,
        },
        presetNodes: {
            // Props with type Object/Array must use a factory function to return the default value.
            default: () => [],
        },
    },
    computed: {
        unlockDateConfig () {
            let maxDate

            this.presetNodes.forEach((node) => {
                if (new Date(node.due_date) < new Date(maxDate) || !maxDate) {
                    maxDate = node.due_date
                }

                if (node.type !== 'p') {
                    if (new Date(node.unlock_date) < new Date(maxDate) || !maxDate) {
                        maxDate = node.unlock_date
                    }

                    if (new Date(node.lock_date) < new Date(maxDate) || !maxDate) {
                        maxDate = node.lock_date
                    }
                }
            })

            if (new Date(this.assignmentDetails.due_date) < new Date(maxDate) || !maxDate) {
                maxDate = this.assignmentDetails.due_date
            }

            if (!maxDate) {
                maxDate = this.assignmentDetails.lock_date
            }

            return Object.assign({}, { maxDate }, this.$root.flatPickrTimeConfig)
        },
        dueDateConfig () {
            let minDate

            this.presetNodes.forEach((node) => {
                if (new Date(node.due_date) > new Date(minDate) || !minDate) {
                    minDate = node.due_date
                }
            })

            if (!minDate) {
                minDate = this.assignmentDetails.unlock_date
            }

            return Object.assign({}, {
                minDate,
                maxDate: this.assignmentDetails.lock_date,
            }, this.$root.flatPickrTimeConfig)
        },
        lockDateConfig () {
            let minDate

            this.presetNodes.forEach((node) => {
                if (new Date(node.due_date) > new Date(minDate) || !minDate) {
                    minDate = node.due_date
                }

                if (node.type !== 'p') {
                    if (new Date(node.unlock_date) > new Date(minDate) || !minDate) {
                        minDate = node.unlock_date
                    }

                    if (new Date(node.lock_date) > new Date(minDate) || !minDate) {
                        minDate = node.lock_date
                    }
                }
            })

            if (new Date(this.assignmentDetails.due_date) > new Date(minDate) || !minDate) {
                minDate = this.assignmentDetails.due_date
            }

            if (!minDate) {
                minDate = this.assignmentDetails.lock_date
            }

            return Object.assign({}, { minDate }, this.$root.flatPickrTimeConfig)
        },
    },
}
</script>
