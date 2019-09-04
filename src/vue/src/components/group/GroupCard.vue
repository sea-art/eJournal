<template>
    <div>
        <b-card
            v-if="editing"
            class="no-hover"
        >
            <b-button
                class="float-right"
                type="submit"
                @click="editing = false"
            >
                <icon name="times"/>
                Stop editing
            </b-button>
            <b-form @submit.prevent="updateGroupName">
                <h2 class="field-heading">
                    Group name
                </h2><br/>
                <div class="d-flex">
                    <b-input
                        v-model="group.name"
                        :readonly="!$hasPermission('can_edit_course_user_group')"
                        class="multi-form  mr-2 theme-input"
                        required
                        placeholder="Group name"
                    />
                    <b-button
                        class="add-button multi-form"
                        type="submit"
                    >
                        <icon name="save"/>
                        Save
                    </b-button>
                </div>
            </b-form>
            <h2 class="field-heading">
                Members
            </h2>
            <ul
                v-if="$hasPermission('can_edit_course_user_group')"
                class="member-list"
            >
                <li
                    v-for="member in members"
                    :key="member.id"
                >
                    <b>{{ member.full_name }}</b> ({{ member.username }})
                    <b-button
                        class="float-right delete-button"
                        type="submit"
                        @click.stop
                        @click="removeUser(member)"
                    >
                        <icon name="user-times"/>
                        Remove
                    </b-button>
                </li>
            </ul>

            <div v-if="$hasPermission('can_edit_course_user_group')">
                <div class="d-flex">
                    <multiselect
                        v-model="participantToAdd"
                        :options="notMembers"
                        :closeOnSelect="true"
                        :customLabel="participantLabel"
                        class="multi-form mr-2"
                        placeholder="Select user to add..."
                        label="participant"
                        trackBy="id"
                    />
                    <b-button
                        class="add-button multi-form"
                        @click.prevent.stop="addToGroup()"
                    >
                        <icon name="user-plus"/>
                        Add
                    </b-button>
                </div>
            </div>

            <b-button
                v-if="$hasPermission('can_delete_course_user_group')"
                class="float-left delete-button"
                @click.prevent.stop="removeGroup()"
            >
                <icon name="trash"/>
                Delete group
            </b-button>
        </b-card>
        <b-card
            v-else
            class="hover"
            @click="editing = true"
        >
            <span class="float-left">
                <h2 class="field-heading">{{ group.name }}</h2>
                {{ members.length }} {{ members.length === 1 ? "member" : "members" }}
            </span>
        </b-card>
    </div>
</template>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="sass">
.member-list
    padding: 0
    margin-bottom: 0
    li
        list-style-type: none
        line-height: 3em
        padding-bottom: 7px
        margin-bottom: 7px
        border-bottom: 1px solid #eee
    li:last-child
        border-bottom: none

</style>

<script>
import groupAPI from '@/api/group.js'
import multiselect from 'vue-multiselect'

export default {
    components: {
        multiselect,
    },
    props: {
        cID: {
            required: true,
        },
        group: {
            required: true,
        },
        participants: {
            required: true,
        },
    },
    data () {
        return {
            form: {
                newGroupName: '',
            },
            editing: false,
            participantToAdd: null,
        }
    },
    computed: {
        notMembers () {
            return this.participants.filter(p => !this.members.map(m => m.id).includes(p.id))
        },
        members () {
            return this.participants.filter(p => p.groups.map(g => g.id).includes(this.group.id))
        },
    },
    methods: {
        updateGroupName () {
            groupAPI.update(this.group.id, {
                name: this.group.name,
            }, { customSuccessToast: 'Successfully updated the group.' })
                .then((group) => {
                    this.group = group
                    this.form.newGroupName = ''
                })
        },
        removeGroup () {
            if (window.confirm(`Are you sure you want to remove ${this.group.name} from this course?`)) {
                groupAPI.delete(this.group.id, { responseSuccessToast: true }).then(() => {
                    this.$emit('delete-group', this.group)
                })
            }
        },
        removeUser (member) {
            groupAPI.removeMember(
                this.group.id,
                member.id,
                { customSuccessToast: `Removed ${member.full_name} from ${this.group.name}.` },
            )
                .then(() => { this.$emit('remove-member', member, this.group) })
        },
        addToGroup () {
            if (this.participantToAdd) {
                groupAPI.addMember(
                    this.group.id,
                    this.participantToAdd.id,
                    { customSuccessToast: `Added ${this.participantToAdd.full_name} to ${this.group.name}.` },
                )
                    .then((participants) => {
                        this.$emit('update-group', participants, this.group)
                        this.participantToAdd = null
                    })
            }
        },
        participantLabel (participant) {
            return participant.full_name
        },
    },
}
</script>
