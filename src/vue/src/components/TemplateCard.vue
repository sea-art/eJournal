<!-- Example of a simple template. -->
<template>
    <div class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                <div v-if="saveEditMode == 'Save'">
                    <b-card class="card main-card noHoverCard" :class="'pink-border'">
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
                                <b-button @click="saveEdit">{{ saveEditMode }} </b-button>
                                <b-button @click="cancel">Cancel</b-button>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
                <div v-else>
                    <b-card class="card main-card noHoverCard" :class="'pink-border'">
                        <b-row>
                            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                                <h2>{{ textbox1 }}</h2>
                                {{ textbox2 }}<br><br>
                                <b-button @click="saveEdit">{{ saveEditMode }} </b-button>
                            </b-col>
                            <b-col id="main-card-right-column" cols="3" lg-cols="12">
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
            </b-col>
        </b-row>
        <comment-card :comment="comment"/>
    </div>
</template>

<script>
import commentCard from '@/components/CommentCard.vue'

export default {
    /* Variables that are needed to fill in the template. */
    props: ['textbox1', 'textbox2', 'date', 'color'],

    data () {
        return {
            saveEditMode: 'Edit',
            tempbox1: this.textbox1,
            tempbox2: this.textbox2,
            tempProps: [],
            comment: 'hoi1000'
        }
    },

    methods: {
        saveEdit: function () {
            if (this.saveEditMode === 'Save') {
                this.saveEditMode = 'Edit'
                this.tempProps = [this.tempbox1, this.tempbox2]
                this.$emit('edit-data', this.tempProps)
            } else {
                this.tempbox1 = this.textbox1
                this.tempbox2 = this.textbox2
                this.saveEditMode = 'Save'
            }
        },
        cancel: function () {
            this.saveEditMode = 'Edit'
        }
    },

    components: {
        'comment-card': commentCard
    }
}

</script>
