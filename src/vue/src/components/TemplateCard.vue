<!-- Example of a simple template. -->
<template>
    <div class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                <div v-if="save == 'Save'">
                    <b-card class="card main-card" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                Subject: <input v-model="tempbox1"><br>
                                Deadline: {{ date }}
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12">
                                Needs grading
                            </b-col>
                        </b-row>
                        <b-row>
                            <br><br><br>
                            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                                Description: <br>
                                <input v-model="tempbox2"><br>
                                <button @click="saveEdit">{{ save }} </button>
                                <button @click="cancel">Cancel</button>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
                <div v-else>
                    <b-card class="card main-card" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <h2>{{ textbox1 }}</h2>
                                {{ textbox2 }}<br>
                                <button @click="saveEdit">{{ save }} </button>
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12">
                                Needs grading
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
            if (this.save == 'Save') {
                this.save = "Edit"
                this.tempProps = [this.tempbox1, this.tempbox2]
                this.$emit('edit-data', this.tempProps)
            } else {
                this.tempbox1 = this.textbox1
                this.tempbox2 = this.textbox2
                this.save = "Save"
            }
        },

        cancel: function () {
            this.save = "Edit"
        }
    }
}

</script>

<style>
.card:hover {
    background-color: white;
}
</style>
