<!-- Example of a simple template. -->
<template>
    <div class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                <div v-if="saveEditMode == 'Save'">
                    <!-- Dit is edit modus. -->
                    <b-card class="card main-card noHoverCard" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <!-- TODO laat hier de header van het template
                                     zien. -->

                                <h2>{{entryNode.entry.template.name}}</h2>
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12" class="right-content">
                                <!-- TODO Hier moet de locatie van het cijfer
                                    en of de mogelijkheid om het cijfer aan te
                                    passen. -->
                                <div v-if="entryNode.entry.grade != 0">
                                    {{ entryNode.entry.grade }}
                                </div>
                                <div v-else>
                                    To be grated
                                </div>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                                <!-- TODO show hier alle data onder elkaar
                                     als een template index matched met
                                     een entry tag overschrijf dit lege veld -->
                                <div v-for="(field, i) in entryNode.entry.template.fields" :key="field.eID">
                                    <div v-if="field.title != ''">
                                        {{ field.title }}:<br>
                                    </div>

                                    <div v-if="field.type=='t'">
                                        <b-textarea v-model="completeContent[i].data"></b-textarea><br>
                                    </div>
                                    <div v-else-if="field.type=='i'">
                                    </div>
                                    <div v-else-if="field.type=='f'">
                                    </div>
                                </div>
                                <b-button @click="saveEdit">{{ saveEditMode }} </b-button>
                                <b-button @click="cancel">Cancel</b-button>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
                <div v-else>
                    Dit is overview modus.
                    {{completeContent}}
                    <b-card class="card main-card noHoverCard" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <!-- TODO laat hier de header van het template
                                     zien. -->
                                <h2>{{entryNode.entry.template.name}}</h2>
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12" class="right-content">
                                <!-- TODO Hier moet de locatie van het cijfer -->

                                <div v-if="entryNode.entry.grade != 0">
                                    {{ entryNode.entry.grade }}
                                </div>
                                <div v-else>
                                    To be graded
                                </div>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                                <!-- TODO show hier alle data onder elkaar
                                     als een template index matched met
                                     een entry tag en overschrijf dit lege veld
                                     dan.

                                     de knop moet een grade knop worden als
                                     docent zijnde, anders moet er edit staan. -->
                                <div v-for="(field, i) in entryNode.entry.template.fields" :key="field.eID">
                                    <div v-if="field.title != ''">
                                        {{ field.title }}:<br>
                                    </div>

                                    <div v-if="field.type=='t'">
                                        {{ completeContent[i].data }}<br>
                                    </div>
                                    <div v-else-if="field.type=='i'">
                                    </div>
                                    <div v-else-if="field.type=='f'">
                                    </div>
                                </div>
                                <b-button @click="saveEdit">{{ saveEditMode }} </b-button>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
            </b-col>
        </b-row>

        <!-- TODO Laad comments hier in. -->
    </div>
</template>

<script>
export default {
    /* Variables that are needed to fill in the template. */
    props: ['entryNode'],

    data () {
        return {
            saveEditMode: 'Edit',
            tempNode: this.entryNode,
            matchEntry: 0,
            completeContent: [],
            //  TODO Werk commenteer functie uit.
            comment: 'hoi1000',
            editedComment: '',
            comments: [{
                message: 'Hoi het is super slecht, ga je schamen!',
                person: 'Peter'
            }, {
                message: 'Hoi het is super goed!',
                person: 'Ptheven'
            }]
        }
    },

    created () {
        this.setContent()
    },

    methods: {
        saveEdit: function () {
            if (this.saveEditMode === 'Save') {
                this.saveEditMode = 'Edit'
                this.tempNode.entry.content = this.completeContent
                this.$emit('edit-node', this.tempNode)
            } else {
                this.tempbox1 = this.textbox1
                this.tempbox2 = this.textbox2
                this.saveEditMode = 'Save'
            }
        },
        cancel: function () {
            this.saveEditMode = 'Edit'
        },
        setContent: function () {
            var checkFound = false

            for (var templateField of this.entryNode.entry.template.fields) {
                checkFound = false
                console.log(templateField)

                for (var content of this.entryNode.entry.content) {
                    if (content.tag === templateField.tag) {
                        this.completeContent.push({
                            data: content.data,
                            tag: content.tag
                        })

                        checkFound = true
                        break
                    }
                }

                if (!checkFound) {
                    console.log(templateField.tag)
                    this.completeContent.push({
                        data: null,
                        tag: templateField.tag
                    })
                }
            }
        }
    }
}

</script>
