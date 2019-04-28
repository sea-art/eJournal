<!--
    Editor for the currently selected preset in the format editor.
    Edits the preset prop directly.
    Various (many!) elements emit a changed event to track whether unsaved changes exist.
-->

<template>
    <b-card
        :class="$root.getBorderClass($route.params.cID)"
        class="no-hover overflow-x-hidden"
    >
        <h2 class="d-inline multi-form">
            Preset
        </h2>
        <b-button
            class="delete-button float-right multi-form"
            @click.prevent="emitDeletePreset"
        >
            <icon name="trash"/>
            Remove
        </b-button>

        <h2 class="field-heading">
            Preset Type
        </h2>
        <b-row class="multi-form">
            <b-col md="6">
                <b-card
                    :class="{'unselected': currentPreset.type !== 'd'}"
                    @click="changePresetType('d')"
                >
                    <b-button
                        :class="{'selected': currentPreset.type === 'd'}"
                        class="change-button preset-type-button float-left mr-3 mt-2 no-hover"
                    >
                        <icon
                            name="calendar"
                            scale="1.8"
                        />
                    </b-button>
                    <div>
                        <b>Entry</b><br/>
                        An entry that should be filled in before a set deadline.
                    </div>
                </b-card>
            </b-col>
            <b-col md="6">
                <b-card
                    :class="{'unselected': currentPreset.type !== 'p'}"
                    @click="changePresetType('p')"
                >
                    <b-button
                        :class="{'selected': currentPreset.type === 'p'}"
                        class="change-button preset-type-button float-left mr-3 mt-2 no-hover"
                    >
                        <icon
                            name="flag-checkered"
                            scale="1.8"
                        />
                    </b-button>
                    <div>
                        <b>Progress</b><br/>
                        A point target to indicate required progress.
                    </div>
                </b-card>
            </b-col>
        </b-row>

        <b-row v-if="currentPreset.type == 'd'">
            <b-col xl="4">
                <h2 class="field-heading">
                    Unlock date
                    <tooltip tip="Students will be able to work on the entry from this date onwards"/>
                </h2>
                <flat-pickr
                    v-model="currentPreset.unlock_date"
                    :config="unlockDateConfig"
                />
            </b-col>
            <b-col xl="4">
                <h2 class="field-heading">
                    Due date
                    <tooltip
                        tip="Students are expected to have finished their entry by this date, but new entries can
                        still be added until the lock date"
                    />
                </h2>
                <flat-pickr
                    v-model="currentPreset.due_date"
                    :config="dueDateConfig"
                />
            </b-col>
            <b-col xl="4">
                <h2 class="field-heading">
                    Lock date
                    <tooltip tip="Students will not be able to fill in the entry anymore after this date"/>
                </h2>
                <flat-pickr
                    v-model="currentPreset.lock_date"
                    :config="lockDateConfig"
                />
            </b-col>
        </b-row>
        <div v-else>
            <h2 class="field-heading">
                Due date
                <tooltip
                    tip="Students are expected to have reached the point target by this date, but new entries can still
                    be added until the assignment lock date"
                />
            </h2>
            <flat-pickr
                v-model="currentPreset.due_date"
                :config="progressDateConfig"
            />
        </div>

        <h2 class="field-heading">
            Description
        </h2>
        <b-textarea
            v-model="currentPreset.description"
            class="multi-form theme-input"
            placeholder="Description"
        />

        <div v-if="currentPreset.type === 'd'">
            <h2 class="field-heading">
                Preset Template
                <tooltip tip="The template students can use for this entry"/>
            </h2>
            <b-form-select
                v-model="currentPreset.template"
                class="multi-form"
            >
                <option
                    disabled
                    value=""
                >
                    Please select a template
                </option>
                <option
                    v-for="template in templates"
                    :key="template.t.tID"
                    :value="template.t"
                >
                    {{ template.t.name }}
                </option>
            </b-form-select>
            <div v-if="currentPreset !== null">
                <h2 class="field-heading">
                    Preview of the {{ currentPreset.template.name }} template
                </h2>
                <b-card class="no-hover">
                    <template-preview :template="currentPreset.template"/>
                </b-card>
            </div>
        </div>
        <div v-else-if="currentPreset.type === 'p'">
            <h2 class="field-heading">
                Point Target
                <tooltip
                    tip="The amount of points students should have achieved by the deadline of this node to be on
                    schedule, new entries can still be added until the assignment's lock date"
                />
            </h2>
            <b-input
                v-model="currentPreset.target"
                type="number"
                class="theme-input"
                placeholder="Amount of points"
                min="0"
            />
        </div>
    </b-card>
</template>

<script>
import templatePreview from '@/components/template/TemplatePreview.vue'
import tooltip from '@/components/assets/Tooltip.vue'

export default {
    components: {
        templatePreview,
        tooltip,
    },
    props: ['currentPreset', 'templates', 'assignmentDetails'],
    data () {
        return {
            templateNames: [],
            prevID: this.currentPreset.id,
        }
    },
    computed: {
        unlockDateConfig () {
            let maxDate

            if (this.currentPreset.due_date) {
                maxDate = this.currentPreset.due_date
            } else if (this.currentPreset.lock_date) {
                maxDate = this.currentPreset.lock_date
            } else if (this.assignmentDetails.due_date) {
                maxDate = this.assignmentDetails.due_date
            } else {
                maxDate = this.assignmentDetails.lock_date
            }

            return Object.assign({}, {
                minDate: this.assignmentDetails.unlock_date,
                maxDate,
            }, this.$root.flatPickrTimeConfig)
        },
        dueDateConfig () {
            let minDate
            let maxDate

            if (this.currentPreset.unlock_date) {
                minDate = this.currentPreset.unlock_date
            } else {
                minDate = this.assignmentDetails.unlock_date
            }

            if (new Date(this.currentPreset.lock_date) < new Date(maxDate) || !maxDate) {
                maxDate = this.currentPreset.lock_date
            }

            if (new Date(this.assignmentDetails.due_date) < new Date(maxDate) || !maxDate) {
                maxDate = this.assignmentDetails.due_date
            }

            if (!maxDate) {
                maxDate = this.assignmentDetails.lock_date
            }

            return Object.assign({}, {
                minDate,
                maxDate,
            }, this.$root.flatPickrTimeConfig)
        },
        lockDateConfig () {
            let minDate

            if (this.currentPreset.due_date) {
                minDate = this.currentPreset.due_date
            } else if (this.currentPreset.unlock_date) {
                minDate = this.currentPreset.unlock_date
            } else {
                minDate = this.assignmentDetails.unlock_date
            }

            return Object.assign({}, {
                minDate,
                maxDate: this.assignmentDetails.lock_date,
            }, this.$root.flatPickrTimeConfig)
        },
        progressDateConfig () {
            const minDate = this.assignmentDetails.unlock_date
            let maxDate

            if (this.assignmentDetails.due_date) {
                maxDate = this.assignmentDetails.due_date
            } else {
                maxDate = this.assignmentDetails.lock_date
            }

            return Object.assign({}, {
                minDate,
                maxDate,
            }, this.$root.flatPickrTimeConfig)
        },
    },
    watch: {
        currentPreset: {
            handler (newPreset) {
                if (newPreset.id === this.prevID) {
                    this.$emit('changed')
                }

                this.prevID = newPreset.id
            },
            deep: true,
        },
    },
    methods: {
        emitDeletePreset () {
            this.$emit('changed')
            if (window.confirm('Are you sure you want to remove this preset from this format?')) {
                this.$emit('delete-preset')
            }
        },
        // Type-specific fields should be set or deleted
        changePresetType (type) {
            this.currentPreset.type = type
            if (type !== 'p') {
                this.currentPreset.target = ''
            }
            if (type === 'd') {
                if (this.templates[0]) {
                    this.$set(this.currentPreset, 'template', this.templates[0].t)
                } else {
                    this.$set(this.currentPreset, 'template', {})
                }
            }
        },
    },
}
</script>
