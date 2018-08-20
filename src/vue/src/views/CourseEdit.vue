<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-card class="no-hover settings-card">
            <h2 class="mb-2">Manage course data</h2>
            <b-form @submit.prevent="onSubmit">
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                    v-model="course.name"
                    placeholder="Course name"
                    required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                    v-model="course.abbr"
                    maxlength="10"
                    placeholder="Course Abbreviation (Max 10 letters)"
                    required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                    v-model="course.startdate"
                    type="date"
                    required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                    v-model="course.enddate"
                    type="date"
                    required/>

                <b-row>
                    <b-col class="d-flex flex-wrap">
                        <b-button v-if="this.$root.canDeleteCourse()"
                            @click.prevent.stop="deleteCourse()"
                            class="delete-button flex-grow-1 multi-form">
                            <icon name="trash"/>
                            Delete Course
                        </b-button>
                        <b-button v-if="this.$root.canEditCourseRoles()"
                            @click.prevent.stop="routeToEditCourseRoles"
                            class="change-button flex-grow-1 multi-form">
                            <icon name="users"/>
                            Manage Roles and Permissions
                        </b-button>
                        <b-button class="add-button flex-grow-1 multi-form"
                            type="submit"
                            v-if="this.$root.canEditCourse()">
                            <icon name="save"/>
                            Save
                        </b-button>
                    </b-col>
                </b-row>
            </b-form>
        </b-card>

        <div v-if="this.participants.length > 0">
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
                            <b-form-select class="flex-grow-1 multi-form" v-model="selectedView" :select-size="1">
                                <option value="enrolled">Enrolled</option>
                                <option value="unenrolled">Unenrolled</option>
                            </b-form-select>
                        </b-col>
                    </b-row>
                    <input class="multi-form theme-input full-width" type="text" v-model="searchVariable" placeholder="Search..."/>
            </b-card>

            <course-participant-card v-if="selectedView === 'enrolled'"
                @delete-participant="deleteParticipantLocally"
                v-for="(p, i) in filteredUsers"
                :class="{ 'input-disabled': p.role === 'Teacher' && numTeachers <= 1 }"
                :key="p.uID"
                :cID="cID"
                :uID="p.uID"
                :index="i"
                :username="p.role"
                :fullName="p.first_name + ' ' + p.last_name"
                :portraitPath="p.picture"
                :role.sync="p.role"/>

            <add-user-card v-if="selectedView === 'unenrolled'"
                @add-participant="addParticipantLocally"
                v-for="p in filteredUsers"
                :key="p.uID"
                :cID="cID"
                :uID="p.uID"
                :username="p.name"
                :fullName="p.first_name + ' ' + p.last_name"
                :portraitPath="p.picture"/>
        </div>

    </content-single-column>
</template>

<script>
import addUsersToCourseCard from '@/components/course/AddUsersToCourseCard.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import courseParticipantCard from '@/components/course/CourseParticipantCard.vue'
import courseApi from '@/api/course.js'
import store from '@/Store'
import icon from 'vue-awesome/components/Icon'

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
            numTeachers: 0
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
        courseApi.get_course_data(this.cID)
            .then(response => {
                this.course = response
            })

        if (this.$root.canViewCourseParticipants()) {
            courseApi.get_users(this.cID)
                .then(response => {
                    this.participants = response.users
                })
        }
    },
    methods: {
        onSubmit () {
            courseApi.update_course(this.cID,
                this.course.name,
                this.course.abbr,
                this.course.startdate,
                this.course.enddate)
                .then(response => {
                    this.course = response
                    this.pageName = this.course.name
                    this.$toasted.success('Updated course')
                    store.clearCache()
                    this.$router.push({
                        name: 'Course',
                        params: {
                            cID: this.cID
                        }
                    })
                })
        },
        deleteCourse () {
            if (confirm('Are you sure you want to delete ' + this.course.name + '?')) {
                courseApi.delete_course(this.cID)
                    .then(response => {
                        this.$router.push({name: 'Home'})
                        this.$toasted.success('Deleted course')
                    })
            }
        },
        deleteParticipantLocally (role, name, picture, uID) {
            this.participants = this.participants.filter(function (item) {
                return uID !== item.uID
            })
            if (this.unenrolledLoaded === true) {
                this.unenrolledStudents.push({ 'role': role,
                    'name': name,
                    'picture': picture,
                    'uID': uID })
            }
        },
        addParticipantLocally (role, name, picture, uID) {
            this.unenrolledStudents = this.unenrolledStudents.filter(function (item) {
                return uID !== item.uID
            })
            this.participants.push({ 'role': role,
                'name': name,
                'picture': picture,
                'uID': uID
            })
        },
        loadUnenrolledStudents () {
            courseApi.get_unenrolled_users(this.cID)
                .then(response => {
                    this.unenrolledStudents = response
                })
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
        filteredUsers: function () {
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
        'icon': icon
    }
}
</script>
