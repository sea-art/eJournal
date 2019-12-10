<template>
    <div>
        <h2 class="field-heading required">
            Name
        </h2>
        <div class="d-flex">
            <b-input
                v-model="assignmentDetails.name"
                class="multi-form theme-input"
                placeholder="Assignment name"
                required
            />
            <b-button
                v-if="assignmentDetails.is_published"
                v-b-tooltip.hover
                class="add-button multi-form ml-2"
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
                class="delete-button multi-form ml-2"
                title="This assignment is not visible to students.
                Once an assignment is published, it cannot be unpublished"
                @click="assignmentDetails.is_published = true"
            >
                <icon name="times"/>
                Unpublished
            </b-button>
        </div>
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
                    class="multi-form"
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
                    class="multi-form"
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
                    class="multi-form"
                    :config="Object.assign({}, {
                        minDate: assignmentDetails.dueDate ? assignmentDetails.dueDate : assignmentDetails.unlockDate
                    }, $root.flatPickrTimeConfig)"
                />
            </b-col>
        </b-row>
        <b-card
            v-if="assignmentDetails.is_group_assignment || !assignmentDetails.id"
            class="no-hover"
        >
            {{ assignment }}
            <template v-if="assignment.journals === null || assignment.journal.length === 0">
                <toggle-switch
                    :isActive="assignmentDetails.is_group_assignment"
                    class="float-right"
                    @parentActive="(isActive) => { assignmentDetails.is_group_assignment = isActive }"
                />
                <h2 class="field-heading multi-form">
                    Group assignment
                </h2>
                Have multiple students contribute to a shared journal.
                Selecting this option requires you to create journals on the assignment page for students to join.
                <hr/>
            </template>
            <template v-if="assignmentDetails.is_group_assignment">
                <toggle-switch
                    :isActive="assignmentDetails.can_lock_journal"
                    class="float-right"
                    @parentActive="(isActive) => { assignmentDetails.can_lock_journal = isActive }"
                />
                <h2 class="field-heading multi-form">
                    Allow locking journal members
                </h2>
                Once the members of a journal are locked, it cannot be joined by other students.
                Teachers can still manually add students to a journal.
                <hr/>
                <toggle-switch
                    :isActive="assignmentDetails.can_set_journal_name"
                    class="float-right"
                    @parentActive="(isActive) => { assignmentDetails.can_set_journal_name = isActive }"
                />
                <h2 class="field-heading">
                    Allow custom journal name
                </h2>
                When selected, members of a journal can override its given name.
                <hr/>
                <toggle-switch
                    :isActive="assignmentDetails.can_set_journal_image"
                    class="float-right"
                    @parentActive="(isActive) => { assignmentDetails.can_set_journal_image = isActive }"
                />
                <h2 class="field-heading">
                    Allow custom display picture
                </h2>
                When selected, members of a journal can override its display picture.
            </template>
        </b-card>
    </div>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'
import tooltip from '@/components/assets/Tooltip.vue'
import toggleSwitch from '@/components/assets/ToggleSwitch.vue'

export default {
    name: 'AssignmentDetails',
    components: {
        textEditor,
        tooltip,
        toggleSwitch,
    },
    props: {
        assignmentDetails: {
            required: true,
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
