<template>
    <div class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                    <b-card class="card main-card noHoverCard" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <h2>Preset Deadline</h2>
                                <b-input class="mb-2 mr-sm-2 mb-sm-0" v-model="deadlineDate" type="date"/>
                                <br/>
                                <b-input class="mb-2 mr-sm-2 mb-sm-0" v-model="deadlineTime" type="time"/>
                                <br/>

                                <h2>Preset Type</h2>
                                <b-form-select v-model="currentPreset.type" @change="onChangePresetType">
                                    <option :value="'d'">Entry</option>
                                    <option :value="'p'">Progress Check</option>
                                </b-form-select>
                                <br/>
                                <br/>

                                <div v-if="currentPreset.type === 'd'">
                                    <h2>Preset Template</h2>
                                    <b-form-select v-model="currentPreset.template">
                                        <option disabled value="">Please select a template</option>
                                        <option v-for="template in templates" :key="template.t.tID" :value="template.t">
                                            {{template.t.name}}
                                        </option>
                                    </b-form-select>
                                    <br><br>
                                    <div v-if="currentPreset !== null">
                                        <h3>Preview</h3>
                                        <template-preview :template="currentPreset.template"/>
                                    </div>
                                </div>
                                <div v-else-if="currentPreset.type === 'p'">
                                    <h2>Point Target</h2>
                                    <b-input class="mb-2 mr-sm-2 mb-sm-0" v-model="currentPreset.target" placeholder="Amount of points"/>
                                </div>
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12">
                            </b-col>
                        </b-row>
                    </b-card>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import templatePreview from '@/components/TemplatePreview.vue'

export default {
    props: ['currentPreset', 'templates'],

    data () {
        return {
            templateNames: []
        }
    },

    computed: {
        deadlineDate: {
            get: function () { return this.currentPreset.deadline.split(' ')[0] },
            set: function (val) { this.currentPreset.deadline = val + ' ' + this.currentPreset.deadline.split(' ')[1] }
        },
        deadlineTime: {
            get: function () { return this.currentPreset.deadline.split(' ')[1] },
            set: function (val) { this.currentPreset.deadline = this.currentPreset.deadline.split(' ')[0] + ' ' + val }
        }
    },

    methods: {
        onChangePresetType (value) {
            if (value !== 'p') {
                this.currentPreset.target = ''
            }
        }
    },

    components: {
        'template-preview': templatePreview
    }
}
</script>
