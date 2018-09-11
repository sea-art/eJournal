<template>
    <div>
        <b-btn class="change-button flex-grow-1 multi-form" v-b-modal="'CourseGroupModal'">Manage Course Groups</b-btn>
        <b-modal id="CourseGroupModal"
                 title="Manage Course Groups"
                 hide-footer>

            <b-card class="no-hover settings-card">
                <h2 class="mb-2">Create new course</h2>
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
            </b-card>

            <group-card
                @delete-group="deleteGroup"
                @update-group="updateGroup"
                v-for="g in groups"
                :key="g.id"
                :cID="cID"
                :group="g.name"/>
        </b-modal>
    </div>
</template>

<script>
import icon from 'vue-awesome/components/Icon'
import groupCard from '@/components/group/GroupCard.vue'
import groupApi from '@/api/group.js'

export default {
    name: 'CourseGroupModal',
    props: {
        cID: {
            required: true
        },
        groups: {
            required: true
        }
    },
    data () {
        return {
            form: {
                groupName: '',
                groupTA: '',
                lti_id: ''
            }
        }
    },
    methods: {
        createUserGroup () {
            groupApi.create({
                name: this.form.groupName,
                cID: this.cID,
                lti_id: this.lti_id
            })
                .then(group => {
                    this.$emit('create-group', group.name)
                    this.$toasted.success('Group creation succes.')
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        resetFormInput (evt) {
            /* Reset our form values */
            this.form.groupName = ''
            this.form.groupTA = ''
        },
        deleteGroup (groupName) {
            this.$emit('delete-group', groupName)
        },
        updateGroup (oldGroupName, newGroupName) {
            this.$emit('update-group', oldGroupName, newGroupName)
        }
    },
    components: {
        'icon': icon,
        'group-card': groupCard
    }
}
</script>
