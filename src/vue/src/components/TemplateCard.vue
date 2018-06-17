<!-- Example of a simple template. -->
<template>
    <div class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                <div v-if="save == 'Save'">
                    <b-card class="card main-card" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <h2>Subject:</h2> <b-textarea v-model="tempbox1"></b-textarea><br>
                                Deadline: {{ date }}
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12" class="right-content">
                                Needs grading
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                                <br>
                                <h2>Description:</h2>
                                <b-textarea v-model="tempbox2"></b-textarea><br><br>
                                <b-button @click="saveEdit">{{ save }} </b-button>
                                <b-button @click="cancel">Cancel</b-button>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
                <div v-else>
                    <b-card class="card main-card" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <h2>{{ textbox1 }}</h2>
                                {{ textbox2 }}<br><br>
                                <b-button @click="saveEdit">{{ save }} </b-button>
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12">
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
            </b-col>
        </b-row>
    </div>
</template>

<script>
export default {
    /* Variables that are needed to fill in the template. */
    props: ['textbox1', 'textbox2', 'date', 'color'],

    data () {
        return {
            save: 'Edit',
            tempbox1: this.textbox1,
            tempbox2: this.textbox2,
            tempProps: []
        }
    },

    methods: {
        saveEdit: function () {
            if (this.save === 'Save') {
                this.save = 'Edit'
                this.tempProps = [this.tempbox1, this.tempbox2]
                this.$emit('edit-data', this.tempProps)
            } else {
                this.tempbox1 = this.textbox1
                this.tempbox2 = this.textbox2
                this.save = 'Save'
            }
        },
        cancel: function () {
            this.save = 'Edit'
        }
    }
}

</script>

<style>
.card:hover {
    background-color: var(--theme-light-grey);
}
</style>
