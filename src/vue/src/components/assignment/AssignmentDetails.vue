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
            placeholder="Enter the description of the assignment here"
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
                    :config="unlockDateConfig"
                />
            </b-col>
            <b-col xl="4">
                <h2 class="field-heading">
                    Due date
                    <tooltip
                        tip="Students are expected to have finished their assignment by this date, but new
                        entries can still be added until the lock date"
                    />
                </h2>
                <flat-pickr
                    v-model="assignmentDetails.due_date"
                    :config="dueDateConfig"
                />
            </b-col>
            <b-col xl="4">
                <h2 class="field-heading">
                    Lock date
                    <tooltip tip="No more entries can be added after this date"/>
                </h2>
                <flat-pickr
                    v-model="assignmentDetails.lock_date"
                    :config="lockDateConfig"
                />
            </b-col>
        </b-row>
        <h2
            v-if="canChangeOptions"
            class="field-heading"
        >
            Options
        </h2>
        <div
            v-if="canChangeOptions"
        >
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
        </div>
        <h2
            v-if="assignmentDetails.is_group_assignment"
            class="field-heading"
        >
            Max group size
        </h2>
        <div v-if="assignmentDetails.is_group_assignment">
            <b-input
                v-model="assignmentDetails.group_size"
                type="number"
                class="multi-form theme-input"
                placeholder="Max group size"
                min="2"
                step="1"
                required
            />
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
        presetNodes: {
            // Props with type Object/Array must use a factory function to return the default value.
            default: () => [],
        },
        canChangeOptions: {
            default: true,
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
    created () {
        // This makes use of null !== false -> true. As a new assignment should have these options available.
        this.canChangeOptions = this.assignmentDetails.is_published !== false
    },
}
</script>
