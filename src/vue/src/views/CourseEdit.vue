<!-- TODO: switching bewett enrolled and unenrolled after adding/removing a user doesnt work. -->
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
                <b-row>
                    <b-col sm="6" class="d-flex flex-wrap">
                        <b-form-select class="flex-grow-1 multi-form" v-model="selectedSortOption" :select-size="1">
                           <option :value="null">Sort by ...</option>
                           <option value="sortFullName">Sort by name</option>
                           <option value="sortUsername">Sort by username</option>
                        </b-form-select>
                    </b-col>
                    <b-col sm="6" class="d-flex flex-wrap">
                        <b-form-select
                            v-if="$hasPermission('can_add_course_participants')"
                            class="flex-grow-1 multi-form"
                            v-model="selectedView"
                            :select-size="1">
                            <option value="enrolled">Enrolled</option>
                            <option value="unenrolled">Unenrolled</option>
                        </b-form-select>
                        <input v-else class="multi-form theme-input full-width" type="text" v-model="searchVariable" placeholder="Search..."/>
                    </b-col>
                </b-row>
                <input
                    v-if="!$hasPermission('can_add_course_participants')"
                    class="multi-form theme-input full-width"
                    type="text"
                    v-model="searchVariable"
                    placeholder="Search..."/>
            </b-card>

            <course-participant-card v-if="selectedView === 'enrolled'"
                @delete-participant="deleteParticipantLocally"
                v-for="(p, i) in filteredUsers"
                :class="{ 'input-disabled': p.role === 'Teacher' && numTeachers <= 1 }"
                :key="p.id"
                :cID="cID"
                :uID="p.id"
                :index="i"
                :username="p.username"
                :fullName="p.name"
                :portraitPath="p.profile_picture"
                :roles="roles"
                :role.sync="p.role"/>

            <add-user-card v-if="selectedView === 'unenrolled'"
                @add-participant="addParticipantLocally"
                v-for="p in filteredUsers"
                :key="p.id"
                :cID="cID"
                :uID="p.id"
                :username="p.username"
                :fullName="p.name"
                :portraitPath="p.profile_picture"/>
        </div>

    </content-single-column>
</template>

<script>
import addUsersToCourseCard from '@/components/course/AddUsersToCourseCard.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import courseParticipantCard from '@/components/course/CourseParticipantCard.vue'

import store from '@/Store'
import icon from 'vue-awesome/components/Icon'
import courseAPI from '@/api/course'
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
            selectedSortOption: null,
            searchVariable: '',
            selectedView: 'enrolled',
            unenrolledLoaded: false,
            numTeachers: 0,
            roles: []
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

        if (this.$hasPermission('can_view_course_participants')) {
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
        deleteParticipantLocally (role, name, picture, uID) {
            this.participants = this.participants.filter(function (item) {
                return uID !== item.id
            })
            if (this.unenrolledLoaded === true) {
                this.unenrolledStudents.push({
                    'role': role,
                    'name': name,
                    'picture': picture,
                    'uID': uID
                })
            }
        },
        addParticipantLocally (role, name, picture, uID) {
            this.unenrolledStudents = this.unenrolledStudents.filter(function (item) {
                return uID !== item.id
            })
            this.participants.push({
                'role': role,
                'name': name,
                'picture': picture,
                'uID': uID
            })
        },
        loadUnenrolledStudents () {
            // TODO: change to unenrolled
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
        }
    },
    computed: {
        filteredUsers () {
            let self = this

            function compareFullName (a, b) {
                var fullNameA = a.first_name + ' ' + a.last_name
                var fullNameB = b.first_name + ' ' + b.last_name

                if (fullNameA < fullNameB) { return -1 }
                if (fullNameA > fullNameB) { return 1 }
                return 0
            }

            function compareUsername (a, b) {
                if (a.name < b.name) { return -1 }
                if (a.name > b.name) { return 1 }
                return 0
            }

            function checkFilter (user) {
                var username = user.username.toLowerCase()
                var fullName = user.first_name.toLowerCase() + ' ' + user.last_name.toLowerCase()
                var searchVariable = self.searchVariable.toLowerCase()

                if (username.includes(searchVariable) ||
                    fullName.includes(searchVariable)) {
                    return true
                } else {
                    return false
                }
            }

            var viewList = this.participants

            /* Switch view list with drop down menu and load unenrolled
               students when accessing other students at first time. */
            if (this.selectedView === 'unenrolled') {
                if (this.unenrolledLoaded === false) {
                    this.loadUnenrolledStudents()
                }
                viewList = this.unenrolledStudents
            }

            /* Filter list based on search input. */
            if (this.selectedSortOption === 'sortFullName') {
                return viewList.filter(checkFilter).sort(compareFullName)
            } else if (this.selectedSortOption === 'sortUsername') {
                return viewList.filter(checkFilter).sort(compareUsername)
            } else {
                return viewList.filter(checkFilter)
            }
        }
    },
    components: {
        'add-user-card': addUsersToCourseCard,
        'bread-crumb': breadCrumb,
        'content-single-column': contentSingleColumn,
        'course-participant-card': courseParticipantCard,
        icon
    }
}
</script>
