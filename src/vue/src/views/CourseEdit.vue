<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-card class="no-hover settings-card">
            <h3>Manage course data</h3>
            <b-form @submit="onSubmit">
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"
                         v-model="course.name"
                         placeholder="Course name"
                         required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"
                         v-model="course.abbr"
                         maxlength="10"
                         placeholder="Course Abbreviation (Max 10 letters)"
                         required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"
                         v-model="course.startdate"
                         type="date"
                         required/>
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"
                         v-model="course.enddate"
                         type="date"
                         required/>

                <b-row>
                    <b-col>
                        <b-button class="add-button"
                                  type="submit"
                                  v-if="this.$root.canEditCourse()"
                            >Update Course
                        </b-button>
                        <b-button v-if="this.$root.canDeleteCourse()"
                                  @click.prevent.stop="deleteCourse()"
                                  class="delete-button">
                            Delete Course
                        </b-button>
                        <b-button v-if="this.$root.canEditCourseRoles()"
                                  @click.prevent.stop="routeToEditCourseRoles"
                                  class="">
                            Edit permissions
                        </b-button>
                    </b-col>
                </b-row>
            </b-form>
        </b-card>

        <b-card class="no-hover settings-card">
            <h3>Manage course students</h3>
                <b-row>
                    <b-col lg="3" sm="6">
                        <b-form-select v-model="selectedSortOption" :select-size="1">
                           <option :value="null">Sort by ...</option>
                           <option value="sortName">Sort on name</option>
                           <option value="sortID">Sort on ID</option>
                        </b-form-select>
                    </b-col>
                    <b-col lg="3" sm="6">
                        <b-form-select v-model="selectedView" :select-size="1">
                            <option value="enrolled">Enrolled</option>
                            <option value="unenrolled">Unenrolled</option>
                        </b-form-select>
                    </b-col>

                    <b-col cols="6">
                        <input type="text" v-model="searchVariable" placeholder="Search .."/>
                    </b-col>
                </b-row>

            </b-card>

        <!-- TODO PROVIDE FULL NAME AND STUDENTNUMBER DATABASE BOYS -->
        <course-participant-card v-if="selectedView == 'enrolled'"
                                 @delete-participant="deleteParticipantLocally"
                                 v-for="(p, i) in filteredUsers"
            :key="p.uID"
            :cID="cID"
            :uID="p.uID"
            :index="i"
            :studentNumber="p.name"
            :name="p.first_name + ' ' + p.last_name"
            :portraitPath="p.picture"
            :role="p.role"/>

        <add-user-card v-if="selectedView == 'unenrolled'"
                                 @add-participant="addParticipantLocally"
                                 v-for="p in filteredUsers"
             :key="p.uID"
             :cID="cID"
             :uID="p.uID"
             :name="p.name"
             :portraitPath="p.picture"/>

    </content-single-column>
</template>

<script>
import addUsersToCourseCard from '@/components/AddUsersToCourseCard.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import courseParticipantCard from '@/components/CourseParticipantCard.vue'
import courseApi from '@/api/course.js'

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
            unenrolledLoaded: false
        }
    },
    created () {
        courseApi.get_course_data(this.cID)
            .then(response => {
                this.course = response
            })

        courseApi.get_users(this.cID)
            .then(response => {
                this.participants = response.users
            })
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
                'uID': uID })
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

            function compareName (a, b) {
                if (a.name < b.name) { return -1 }
                if (a.name > b.name) { return 1 }
                return 0
            }

            function compareID (a, b) {
                if (a.uID < b.uID) { return -1 }
                if (a.uID > b.uID) { return 1 }
                return 0
            }

            function filterTeacher (user) {
                return user.role !== 'Teacher'
            }

            function checkFilter (user) {
                var userName = user.name.toLowerCase()
                var userID = String(user.uID).toLowerCase()

                if (userName.includes(self.searchVariable.toLowerCase()) ||
                    userID.includes(self.searchVariable)) {
                    return true
                } else {
                    return false
                }
            }

            /* Filter list on teachers. */
            var viewList = this.participants.filter(filterTeacher)

            /* Switch view list with drop down menu and load unenrolled
               students when accessing other students at first time. */
            if (this.selectedView === 'unenrolled') {
                if (this.unenrolledLoaded === false) {
                    this.loadUnenrolledStudents()
                }
                viewList = this.unenrolledStudents
            }

            /* Filter list based on search input. */
            if (this.selectedSortOption === 'sortName') {
                return viewList.filter(checkFilter).sort(compareName)
            } else if (this.selectedSortOption === 'sortID') {
                return viewList.filter(checkFilter).sort(compareID)
            } else {
                return viewList.filter(checkFilter)
            }
        }
    },
    components: {
        'add-user-card': addUsersToCourseCard,
        'bread-crumb': breadCrumb,
        'content-single-column': contentSingleColumn,
        'course-participant-card': courseParticipantCard
    }
}
</script>

<style>
#pushBot {
    margin-bottom: 10px;
}
</style>
