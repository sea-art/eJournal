<template>
    <b-card class="no-hover">
        <b-form
            @submit.prevent="onSubmit"
            @reset.prevent="onReset"
        >
            <div class="d-flex float-right multi-form">
                <b-button
                    v-if="form.isPublished"
                    v-b-tooltip.hover
                    class="add-button flex-grow-1"
                    title="This assignment is visible to students"
                    @click="form.isPublished = false"
                >
                    <icon name="check"/>
                    Published
                </b-button>
                <b-button
                    v-if="!form.isPublished"
                    v-b-tooltip.hover
                    class="delete-button flex-grow-1"
                    title="This assignment is not visible to students"
                    @click="form.isPublished = true"
                >
                    <icon name="times"/>
                    Unpublished
                </b-button>
            </div>

            <h2 class="theme-h2 field-heading required">
                Assignment Name
            </h2>
            <b-input
                v-model="form.assignmentName"
                class="multi-form theme-input"
                placeholder="Assignment name"
                required
            />
            <h2 class="theme-h2 field-heading">
                Description
            </h2>
            <text-editor
                :id="'text-editor-assignment-description'"
                v-model="form.assignmentDescription"
                :footer="false"
                class="multi-form"
                placeholder="Description of the assignment"
            />
            <h2 class="theme-h2 field-heading required">
                Points possible
                <tooltip
                    tip="The amount of points that represents a perfect score for this assignment, excluding bonus
                    points"
                />
            </h2>
            <b-input
                v-model="form.pointsPossible"
                class="multi-form theme-input"
                placeholder="Points"
                type="number"
            />
            <b-row>
                <b-col xl="4">
                    <h2 class="theme-h2 field-heading">
                        Unlock date
                        <tooltip tip="Students will be able to work on the assignment from this date onwards"/>
                    </h2>
                    <flat-pickr
                        v-model="form.unlockDate"
                        :config="unlockDateConfig"
                    />
                </b-col>
                <b-col xl="4">
                    <h2 class="theme-h2 field-heading">
                        Due date
                        <tooltip
                            tip="Students are expected to have finished their assignment by this date, but new entries
                            can still be added until the lock date"
                        />
                    </h2>
                    <flat-pickr
                        v-model="form.dueDate"
                        :config="dueDateConfig"
                    />
                </b-col>
                <b-col xl="4">
                    <h2 class="theme-h2 field-heading">
                        Lock date
                        <tooltip tip="No more entries can be added after this date"/>
                    </h2>
                    <flat-pickr
                        v-model="form.lockDate"
                        :config="lockDateConfig"
                    />
                </b-col>
            </b-row>
            <b-button
                class="float-left change-button mt-2"
                type="reset"
            >
                <icon name="undo"/>
                Reset
            </b-button>
            <b-button
                class="float-right add-button mt-2"
                type="submit"
            >
                <icon name="plus-square"/>
                Create
            </b-button>
        </b-form>
    </b-card>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'
import tooltip from '@/components/assets/Tooltip.vue'

import assignmentAPI from '@/api/assignment.js'

export default {
    name: 'CreateAssignment',
    components: {
        textEditor,
        tooltip,
    },
    props: ['lti', 'page'],
    data () {
        return {
            form: {
                assignmentName: '',
                assignmentDescription: '',
                courseID: '',
                ltiAssignID: null,
                pointsPossible: null,
                unlockDate: null,
                dueDate: null,
                lockDate: null,
                isPublished: false,
            },
        }
    },
    computed: {
        unlockDateConfig () {
            const additionalConfig = {}
            if (this.form.dueDate) {
                additionalConfig.maxDate = new Date(this.form.dueDate)
            } else if (this.form.lockDate) {
                additionalConfig.maxDate = new Date(this.form.lockDate)
            }
            return Object.assign({}, additionalConfig, this.$root.flatPickrTimeConfig)
        },
        dueDateConfig () {
            const additionalConfig = {}
            if (this.form.unlockDate) {
                additionalConfig.minDate = new Date(this.form.unlockDate)
            }
            if (this.form.lockDate) {
                additionalConfig.maxDate = new Date(this.form.lockDate)
            }
            return Object.assign({}, additionalConfig, this.$root.flatPickrTimeConfig)
        },
        lockDateConfig () {
            const additionalConfig = {}
            if (this.form.dueDate) {
                additionalConfig.minDate = new Date(this.form.dueDate)
            } else if (this.form.unlockDate) {
                additionalConfig.minDate = new Date(this.form.unlockDate)
            }
            return Object.assign({}, additionalConfig, this.$root.flatPickrTimeConfig)
        },
    },
    mounted () {
        if (this.lti !== undefined) {
            this.form.assignmentName = this.lti.ltiAssignName
            this.form.ltiAssignID = this.lti.ltiAssignID
            this.form.pointsPossible = this.lti.ltiPointsPossible
            this.form.unlockDate = this.lti.ltiAssignUnlock.slice(0, -9)
            this.form.dueDate = this.lti.ltiAssignDue.slice(0, -9)
            this.form.lockDate = this.lti.ltiAssignLock.slice(0, -9)
            this.form.courseID = this.page.cID
            this.form.isPublished = this.lti.ltiAssignPublished
        } else {
            this.form.courseID = this.$route.params.cID
        }
    },
    methods: {
        onSubmit () {
            assignmentAPI.create({
                name: this.form.assignmentName,
                description: this.form.assignmentDescription,
                course_id: this.form.courseID,
                lti_id: this.form.ltiAssignID,
                points_possible: this.form.pointsPossible,
                unlock_date: this.form.unlockDate,
                due_date: this.form.dueDate,
                lock_date: this.form.lockDate,
                is_published: this.form.isPublished,
            })
                .then((assignment) => {
                    this.$emit('handleAction', assignment.id)
                    this.onReset(undefined)
                    this.$store.dispatch('user/populateStore').catch(() => {
                        this.$toasted.error('The website might be out of sync, please login again.')
                    })
                })
        },
        onReset (evt) {
            if (evt !== undefined) {
                evt.preventDefault()
            }
            /* Reset our form values */
            this.form.assignmentName = ''
            this.form.assignmentDescription = ''
            this.form.unlockDate = undefined
            this.form.dueDate = undefined
            this.form.lockDate = undefined
            this.form.isPublished = false

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        },
    },
}
</script>
