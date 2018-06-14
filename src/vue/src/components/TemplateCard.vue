<!-- Example of a simple template. -->
<template>
    <b-card class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                <div v-if="save == 'Save'">
                    edit modus<br>
                    <input v-model="tempbox1"><br>
                    <input v-model="tempbox2">
                </div>
                <div v-else>
                    <h3>{{ textbox1 }}</h3>
                    <p>{{ textbox2 }}</p><br>
                </div>
                <button @click="saveEdit">{{ save }} </button>
                <button @click="cancel">Cancel</button>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    /* Variables that are needed to fill in the template. */
    props: ['textbox1', 'textbox2', 'date'],

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
.entry-template {
    background-color: var(--theme-light-grey);
}
</style>
