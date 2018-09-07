<template>
    <div>
        <b-btn class="change-button flex-grow-1 multi-form" v-b-modal="'CourseGroupModal'">Manage Course Groups</b-btn>

        <b-modal id="courseGroupModal"
                 title="Manage Course Groups"
                 hide-footer
                 >

            <b-form @submit.prevent="createUserGroup" @reset.prevent="resetFormInput">
                <b-input class="multi-form theme-input" v-model="form.groupName" placeholder="Desired group name" required/>
                <b-input class="multi-form theme-input" v-model="form.groupTA" placeholder="TA name" required/>
                    <b-button class="float-left change-button" type="reset">
                    <icon name="undo"/>
                    Reset
                </b-button>
                <b-button class="float-right add-button" type="submit">
                    <icon name="plus-square"/>
                    Create
                </b-button>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
import groupApi from '@/api/group.js'
import icon from 'vue-awesome/components/Icon'
export default {
    name: 'CourseGroupModal',
    props: {
        cID: {
            required: true
        }
    },
    data () {
        return {
            form: {
                groupName: '',
                groupTA: ''
            }
        }
    },
    methods: {
        createUserGroup () {
            groupApi.create({
                name: this.form.groupName,
                cID: this.cID
            })
                .then(group => {
                    this.$emit('create-group', group.name)
                    this.$toasted.success('Group creation succes.')
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        resetFormInput (evt) {
            /* Reset our form values */
            this.form.groupName = null
            this.form.groupTA = null
            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    },
    components: {
        'icon': icon
    }
}
</script>
