<template>
    <div>
        <h4 class="mb-2"><span>Groups</span></h4>
        <group-card
            @delete-group="deleteGroup"
            @update-group="updateGroup"
            @remove-member="removeMember"
            v-for="g in groups"
            :key="g.id"
            :participants="participants"
            :cID="course.id"
            :group="g"/>

        <div v-if="$hasPermission('can_add_course_user_group')">
            <h4 class="mb-2"><span>Create new group</span></h4>
            <b-card class="no-hover">
                <b-form @submit.prevent="createUserGroup" @reset.prevent="resetFormInput" class="d-flex">
                    <b-input class="new-group-input multi-form mr-2 theme-input" v-model="form.groupName" placeholder="Desired group name" required/>
                    <b-button class="add-button" type="submit">
                        <icon name="plus-square"/>
                        Create
                    </b-button>
                </b-form>
                <b-button v-if="this.course.lti_linked" class="lti-sync multi-form mr-2" type="submit"  @click.prevent.stop="getDataNoseGroups()">
                    <icon name="sync-alt"/>
                    Sync from DataNose
                </b-button>
            </b-card>
        </div>
    </div>
</template>
<style lang="sass">
.new-group-input
    margin-bottom: 0px !important

.lti-sync
    margin-bottom: 0px !important
    margin-top: 10px !important
</style>
<script>
import icon from 'vue-awesome/components/Icon'
import groupCard from '@/components/group/GroupCard.vue'
import groupAPI from '@/api/group'
import participationAPI from '@/api/participation'

export default {
    name: 'CourseGroupEditor',
    props: {
        course: {
            required: true
        }
    },
    data () {
        return {
            form: {
                groupName: '',
                lti_id: ''
            },
            participants: [],
            groups: []
        }
    },
    created () {
        groupAPI.getAllFromCourse(this.course.id)
            .then(groups => { this.groups = groups })
        participationAPI.getEnrolled(this.course.id)
            .then(participants => { this.participants = participants })
    },
    methods: {
        getDataNoseGroups () {
            groupAPI.getDataNose(this.course.id, {customSuccessToast: 'Successfully syncronized from DataNose.'})
        },
        createUserGroup () {
            groupAPI.create({name: this.form.groupName, course_id: this.course.id, lti_id: this.course.lti_id},
                {customSuccessToast: 'Successfully created group.'})
                .then(group => {
                    this.groups.push(group)
                    this.resetFormInput()
                })
        },
        resetFormInput (evt) {
            /* Reset our form values */
            this.form.groupName = ''
        },
        deleteGroup (group) {
            this.groups = this.groups.filter(g => g.id !== group.id)
        },
        updateGroup (participants, group) {
            this.participants = participants
            this.$emit('update-group', group)
        },
        removeMember (member, group) {
            for (let i in this.participants) {
                if (this.participants[i].id === member.id) {
                    this.participants[i].groups = this.participants[i].groups.filter(g => g.id !== group.id)
                }
            }
            this.participants = this.participants
        }
    },
    components: {
        icon,
        'group-card': groupCard
    }
}
</script>
