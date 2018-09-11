<!-- TODO: You shouldnt be able to change your own role. -->
<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-card class="no-hover settings-card">
            <h2 class="mb-2">Manage course data</h2>

            <b-form @submit.prevent="onSubmit">
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                    :readonly="!$hasPermission('can_edit_course')"
                    v-model="course.name"
                    placeholder="Course name"
                    required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                    :readonly="!$hasPermission('can_edit_course')"
                    v-model="course.abbreviation"
                    maxlength="10"
                    placeholder="Course Abbreviation (Max 10 letters)"
                    required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                    :readonly="!$hasPermission('can_edit_course')"
                    v-model="course.startdate"
                    type="date"
                    required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                    :readonly="!$hasPermission('can_edit_course')"
                    v-model="course.enddate"
                    type="date"
                    required/>

                <b-row>
                    <b-col class="d-flex flex-wrap">
                        <b-button v-if="$hasPermission('can_delete_course')"
                            @click.prevent.stop="deleteCourse()"
                            class="delete-button flex-grow-1 multi-form">
                            <icon name="trash"/>
                            Delete Course
                        </b-button>
                        <b-button v-if="$hasPermission('can_edit_course_roles')"
                            @click.prevent.stop="routeToEditCourseRoles"
                            class="change-button flex-grow-1 multi-form">
                            <icon name="users"/>
                            Manage Roles and Permissions
                        </b-button>
                        <group-modal v-if="$hasPermission('can_edit_course')"
                                     :cID="this.cID"
                                     :groups="this.groups"
                                     @create-group="createGroup"
                                     @delete-group="deleteGroup"
                                     @update-group="updateGroup">
                        </group-modal>

                        <b-button class="add-button flex-grow-1 multi-form"
                            type="submit"
                            v-if="$hasPermission('can_edit_course')">
                            <icon name="save"/>
                            Save
                        </b-button>
                    </b-col>
                </b-row>
            </b-form>
        </b-card>

        <div>
            <b-card class="no-hover">
                <h2 class="mb-2">Manage course members</h2>
                <b-row v-if="$hasPermission('can_add_course_participants')">
                    <b-col sm="12">
                        <input class="theme-input full-width multi-form" type="text" v-model="searchVariable" placeholder="Search..."/>
                    </b-col>
                    <b-col sm="12" class="d-flex flex-wrap">
                        <b-button v-if="viewEnrolled" v-on:click.stop @click="toggleEnroled" class="button full-width multi-form">
                            View unenrolled users
                        </b-button>
                        <b-button v-if="!viewEnrolled" v-on:click.stop @click="toggleEnroled" class="button full-width multi-form">
                            View enrolled participants
                        </b-button>
                    </b-col>
                    <b-col sm="8" class="d-flex flex-wrap">
                        <b-form-select class="multi-form" v-model="selectedSortOption" :select-size="1">
                            <option :value="null">Sort by ...</option>
                            <option value="sortFullName">Sort by name</option>
                            <option value="sortUsername">Sort by username</option>
                        </b-form-select>
                    </b-col>
                    <b-col sm="8" class="d-flex flex-wrap">
                        <b-form-select v-model="selectedFilterGroupOption"
                                       :select-size="1">
                            <option :value="null">Filter group by ...</option>
                            <option v-for="group in groups" :key="group.name" :value="group.name">
                                {{ group.name }}
                            </option>
                        </b-form-select>
                    </b-col>
                    <b-col sm="4">
                        <b-button v-on:click.stop v-if="!order" @click="toggleOrder" class="button full-width multi-form">
                            <icon name="long-arrow-down"/>
                            Ascending
                        </b-button>
                        <b-button v-on:click.stop v-if="order" @click="toggleOrder" class="button full-width multi-form">
                            <icon name="long-arrow-up"/>
                            Descending
                        </b-button>
                    </b-col>
                </b-row>
            </b-card>

            <course-participant-card v-if="viewEnrolled"
                @delete-participant="deleteParticipantLocally"
                v-for="p in filteredUsers"
                :class="{ 'input-disabled': p.role === 'Teacher' && numTeachers <= 1 }"
                :key="p.id"
                :cID="cID"
                :group.sync="p.group"
                :groups="groups"
                :user="p"
                :roles="roles"/>

            <add-user-card v-if="!viewEnrolled"
                @add-participant="addParticipantLocally"
                v-for="p in filteredUsers"
                :key="p.id"
                :cID="cID"
                :user="p"/>
        </div>
    </content-single-column>
</template>

<script>
import addUsersToCourseCard from '@/components/course/AddUsersToCourseCard.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import courseParticipantCard from '@/components/course/CourseParticipantCard.vue'
import groupModal from '@/components/course/CourseGroupModal.vue'

import store from '@/Store'
import icon from 'vue-awesome/components/Icon'
import courseAPI from '@/api/course'
import groupAPI from '@/api/group'
import roleAPI from '@/api/role'
import participationAPI from '@/api/participation'

export default {
    name: 'CourseEdit',
    props: {
        cID: {
            required: true
        }
    },
    data () {
        return {
            course: {},
            form: {},
            participants: [],
            unenrolledStudents: [],
            groups: [],
            selectedSortOption: null,
            selectedFilterGroupOption: null,
            searchVariable: '',
            unenrolledLoaded: false,
            numTeachers: 0,
            roles: [],
            viewEnrolled: true,
            order: false
        }
    },
    watch: {
        participants: {
            handler: function (val, _) {
                this.numTeachers = val.filter(p => p.role === 'Teacher').length
            },
            deep: true
        }
    },
    created () {
        courseAPI.get(this.cID)
            .then(course => { this.course = course })
            .catch(error => { this.$toasted.error(error.response.data.description) })

        groupAPI.getAllFromCourse(this.cID)
            .then(groups => { this.groups = groups })
            .catch(error => { this.$toasted.error(error.response.data.description) })

        roleAPI.getFromCourse(this.cID)
            .then(roles => { this.roles = roles })
            .catch(error => { this.$toated.error(error.response.data.description) })

        if (this.$hasPermission('can_view_course_participants')) {
            roleAPI.getFromCourse(this.cID)
                .then(roles => { this.roles = roles })
                .catch(error => { this.$toasted.error(error.response.data.description) })

            participationAPI.getEnrolled(this.cID)
                .then(users => { this.participants = users })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        }
    },
    methods: {
        onSubmit () {
            courseAPI.update(this.cID, this.course)
                .then(course => {
                    this.course = course
                    this.$toasted.success('Succesfully updated the course.')
                    store.clearCache()
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        deleteCourse () {
            if (confirm('Are you sure you want to delete ' + this.course.name + '?')) {
                courseAPI.delete(this.cID)
                    .then(response => {
                        this.$router.push({name: 'Home'})
                        this.$toasted.success(response.description)
                    })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        },
        deleteParticipantLocally (user) {
            this.participants = this.participants.filter(function (item) {
                return user.id !== item.id
            })
            if (this.unenrolledLoaded === true) {
                this.unenrolledStudents.push(user)
            }
        },
        addParticipantLocally (user) {
            this.unenrolledStudents = this.unenrolledStudents.filter(function (item) {
                return user.id !== item.id
            })
            user.role = 'Student'
            this.participants.push(user)
        },
        createGroup (groupName) {
            this.groups.push({
                'name': groupName
            })
        },
        deleteGroup (groupName) {
            this.groups = this.groups.filter(function (item) {
                return groupName !== item.name
            })

            // TODO replace api function with frontend function
            if (this.$hasPermission('can_view_course_participants')) {
                participationAPI.getEnrolled(this.cID)
                    .then(users => { this.participants = users })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        },
        updateGroup (oldGroupName, newGroupName) {
            // TODO replace api function with frontend function
            groupAPI.getAllFromCourse(this.cID)
                .then(groups => { this.groups = groups })
                .catch(error => { this.$toasted.error(error.response.data.description) })

            if (this.$hasPermission('can_view_course_participants')) {
                participationAPI.getEnrolled(this.cID)
                    .then(users => { this.participants = users })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        },
        loadUnenrolledStudents () {
            participationAPI.getUnenrolled(this.cID)
                .then(users => { this.unenrolledStudents = users })
                .catch(error => { this.$toasted.error(error.response.data.description) })
            this.unenrolledLoaded = !this.unenrolledLoaded
        },
        routeToEditCourseRoles () {
            this.$router.push({
                name: 'UserRoleConfiguration',
                params: { cID: this.cID }
            })
        },
        compare (a, b) {
            if (a < b) { return this.order ? 1 : -1 }
            if (a > b) { return this.order ? -1 : 1 }
            return 0
        },
        toggleOrder () {
            this.order = !this.order
        },
        toggleEnroled () {
            this.viewEnrolled = !this.viewEnrolled
        }
    },
    computed: {
        filteredUsers () {
            let self = this

            function compareFullName (a, b) {
                return self.compare(a.name, b.name)
            }

            function compareUsername (a, b) {
                return self.compare(a.username, b.username)
            }

            function searchFilter (user) {
                var username = user.username.toLowerCase()
                var fullName = user.first_name.toLowerCase() + ' ' + user.last_name.toLowerCase()
                var searchVariable = self.searchVariable.toLowerCase()

                return username.includes(searchVariable) ||
                       fullName.includes(searchVariable)
            }

            function checkGroup (user) {
                if (self.selectedFilterGroupOption) {
                    if (!user.group) {
                        return user.group === self.selectedFilterGroupOption
                    } else {
                        return user.group.includes(self.selectedFilterGroupOption)
                    }
                }

                return true
            }

            var viewList = this.participants

            /* Switch view list with drop down menu and load unenrolled
               students when accessing other students at first time. */
            if (!this.viewEnrolled) {
                if (this.unenrolledLoaded === false) {
                    this.loadUnenrolledStudents()
                }
                viewList = this.unenrolledStudents
            }

            /* Filter list based on search input. */
            if (this.selectedSortOption === 'sortFullName') {
                viewList = viewList.sort(compareFullName)
            } else if (this.selectedSortOption === 'sortUsername') {
                viewList = viewList.sort(compareUsername)
            }

            return viewList.filter(searchFilter).filter(checkGroup)
        }
    },
    components: {
        'add-user-card': addUsersToCourseCard,
        'bread-crumb': breadCrumb,
        'content-single-column': contentSingleColumn,
        'course-participant-card': courseParticipantCard,
        'group-modal': groupModal,
        icon
    }
}
</script>
