<!-- TODO: You shouldnt be able to change your own role. -->
<template>
    <content-columns>
        <bread-crumb slot="main-content-column"/>

        <div v-if="activeView === 'courseData'" slot="main-content-column">
            <h4 class="mb-2"><span>Manage course details</span></h4>
            <b-card class="no-hover multi-form" :class="$root.getBorderClass($route.params.uID)">
                <b-form @submit.prevent="onSubmit">
                    <h2 class="field-heading required">Course name</h2>
                    <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                        :readonly="!$hasPermission('can_edit_course_details')"
                        v-model="course.name"
                        placeholder="Course name"/>
                    <h2 class="field-heading required">Course abbreviation</h2>
                    <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                        :readonly="!$hasPermission('can_edit_course_details')"
                        v-model="course.abbreviation"
                        maxlength="10"
                        placeholder="Course abbreviation (max 10 characters)"/>
                    <b-row>
                        <b-col xs="6">
                            <h2 class="field-heading required">
                                From
                                <tooltip tip="Start date of the course" />
                            </h2>
                            <flat-pickr class="multi-form theme-input full-width"
                                :class="{ 'input-disabled': !$hasPermission('can_edit_course_details') }"
                                v-model="course.startdate"/>
                        </b-col>
                        <b-col xs="6">
                            <h2 class="field-heading required">
                                To
                                <tooltip tip="End date of the course" />
                            </h2>
                            <flat-pickr class="multi-form theme-input full-width"
                                :class="{ 'input-disabled': !$hasPermission('can_edit_course_details') }"
                                v-model="course.enddate"/>
                        </b-col>
                    </b-row>
                    <b-button class="add-button float-right"
                        type="submit"
                        v-if="$hasPermission('can_edit_course_details')">
                        <icon name="save"/>
                        Save
                    </b-button>
                </b-form>
            </b-card>
        </div>

        <div v-if="activeView === 'courseMembers'" slot="main-content-column">
            <h4 class="mb-2"><span>Manage course members</span></h4>
            <div class="d-flex">
                <input
                    v-if="viewEnrolled"
                    class="theme-input flex-grow-1 no-width multi-form mr-2"
                    type="text"
                    v-model="searchValue"
                    placeholder="Search..."/>
                <input
                    v-if="!viewEnrolled"
                    class="theme-input flex-grow-1 no-width multi-form mr-2"
                    type="text"
                    v-model="unenrolledQuery"
                    placeholder="Name or username with at least 5 characters"
                    @keyup.enter="searchUnenrolled"/>
                <b-button
                    v-if="!viewEnrolled"
                    class="multi-form mr-2"
                    @click="searchUnenrolled">
                    <icon name="search"/>
                    Search users
                </b-button>
                <b-button v-if="viewEnrolled" v-on:click.stop @click="toggleEnrolled" class="multi-form">
                    <icon name="users"/>
                    Enrolled
                </b-button>
                <b-button v-if="!viewEnrolled" v-on:click.stop @click="toggleEnrolled" class="multi-form">
                    <icon name="user-plus"/>
                    Unenrolled
                </b-button>
            </div>
            <div class="d-flex">
                <b-form-select class="multi-form mr-2" v-model="selectedSortOption" :select-size="1">
                    <option value="name">Sort by name</option>
                    <option value="username">Sort by username</option>
                </b-form-select>
                <b-form-select class="multi-form mr-2" v-model="groupFilter"
                               :select-size="1">
                    <option :value="null">Filter group by ...</option>
                    <option v-for="group in groups" :key="group.name" :value="group.name">
                        {{ group.name }}
                    </option>
                </b-form-select>
                <b-button v-on:click.stop v-if="!order" @click="setOrder(!order)" class="multi-form">
                    <icon name="long-arrow-down"/>
                    Ascending
                </b-button>
                <b-button v-on:click.stop v-if="order" @click="setOrder(!order)" class="multi-form">
                    <icon name="long-arrow-up"/>
                    Descending
                </b-button>
            </div>
            <b-col sm="8" class="d-flex flex-wrap">
            </b-col>
            <b-card class="no-hover" v-if="!viewEnrolled && !this.unenrolledStudents.length">
                <div class="float-left">
                    <b>{{ unenrolledQueryDescription }}</b>
                </div>
            </b-card>

            <course-participant-card v-if="viewEnrolled"
                @delete-participant="deleteParticipantLocally"
                @update-participants="updateParticipants"
                v-for="p in filteredUsers"
                :key="p.id"
                :cID="cID"
                :group.sync="p.group"
                :groups="groups"
                :user="p"
                :numTeachers="numTeachers"
                :roles="roles"/>

            <add-user-card v-if="!viewEnrolled"
                @add-participant="addParticipantLocally"
                v-for="p in filteredUsers"
                :key="p.id"
                :cID="cID"
                :user="p"/>
        </div>

        <div slot="right-content-column">
            <h3>Actions</h3>
            <b-button v-if="$hasPermission('can_edit_course_details')"
                class="multi-form change-button full-width"
                @click="activeView = 'courseData'">
                <icon name="edit"/>
                Manage Details
            </b-button>
            <b-button v-if="$hasPermission('can_edit_course_details')"
                class="multi-form change-button full-width"
                @click="activeView = 'courseMembers'">
                <icon name="user"/>
                Manage Members
            </b-button>
            <b-button v-if="$hasPermission('can_edit_course_details')"
                class="multi-form change-button full-width"
                @click="activeView = 'courseGroups'">
                <icon name="users"/>
                Manage Groups
            </b-button>
            <b-button v-if="$hasPermission('can_edit_course_roles')"
                @click.prevent.stop="routeToEditCourseRoles"
                class="multi-form change-button full-width">
                <icon name="cog"/>
                Manage Permissions
            </b-button>
            <b-button v-if="$hasPermission('can_delete_course')"
                @click.prevent.stop="deleteCourse()"
                class="multi-form delete-button full-width">
                <icon name="trash"/>
                Delete Course
            </b-button>
        </div>

        <group-editor
            v-if="activeView === 'courseGroups'"
            slot="main-content-column"
            :cID="this.cID"
            :groups="this.groups"
            :lti_linked="this.course.lti_linked"
            :lti_id="this.course.lti_id"
            @create-group="createGroup"
            @delete-group="deleteGroup"
            @update-group="updateGroup"
            @update-groups="updateGroups"/>
    </content-columns>
</template>

<script>
import addUsersToCourseCard from '@/components/course/AddUsersToCourseCard.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import contentColumns from '@/components/columns/ContentColumns.vue'
import courseParticipantCard from '@/components/course/CourseParticipantCard.vue'
import groupEditor from '@/components/course/CourseGroupEditor.vue'
import tooltip from '@/components/assets/Tooltip.vue'

import store from '@/Store'
import icon from 'vue-awesome/components/Icon'
import courseAPI from '@/api/course'
import groupAPI from '@/api/group'
import roleAPI from '@/api/role'
import participationAPI from '@/api/participation'
import { mapGetters, mapMutations } from 'vuex'

export default {
    name: 'CourseEdit',
    props: {
        cID: {
            required: true
        }
    },
    data () {
        return {
            activeView: 'courseData',
            course: {},
            originalCourse: {},
            participants: [],
            unenrolledStudents: [],
            groups: [],
            unenrolledLoaded: false,
            numTeachers: 0,
            roles: [],
            unenrolledQuery: '',
            unenrolledQueryDescription: 'Search unenrolled users in the search field above.'
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
            .then(course => {
                this.course = course
                this.originalCourse = this.deepCopyCourse(course)
            })

        groupAPI.getAllFromCourse(this.cID)
            .then(groups => { this.groups = groups })

        roleAPI.getFromCourse(this.cID)
            .then(roles => { this.roles = roles })

        if (this.$hasPermission('can_view_course_users')) {
            roleAPI.getFromCourse(this.cID)
                .then(roles => { this.roles = roles })

            participationAPI.getEnrolled(this.cID)
                .then(users => { this.participants = users })
        }
    },
    methods: {
        ...mapMutations({
            setOrder: 'preferences/SET_COURSE_MEMBERS_SORT_ASCENDING',
            setViewEnrolled: 'preferences/SET_COURSE_MEMBERS_VIEW_ENROLLED',
            setCourseMembersGroupFilter: 'preferences/SET_COURSE_MEMBERS_GROUP_FILTER',
            setCourseMembersSearchValue: 'preferences/SET_COURSE_MEMBERS_SEARCH_VALUE',
            setCourseMembersSortBy: 'preferences/SET_COURSE_MEMBERS_SORT_BY'
        }),
        formFilled () {
            return this.course.name && this.course.abbreviation && this.course.startdate && this.course.enddate
        },
        onSubmit () {
            if (this.formFilled()) {
                courseAPI.update(this.cID, this.course, {customSuccessToast: 'Successfully updated the course.'})
                    .then(course => {
                        this.course = course
                        this.originalCourse = this.deepCopyCourse(course)
                        store.clearCache()
                    })
            } else {
                this.$toasted.error('One or more required fields are empty.')
            }
        },
        deleteCourse () {
            if (confirm('Are you sure you want to delete ' + this.course.name + '?')) {
                courseAPI.delete(this.cID)
                    .then(response => { this.$router.push({name: 'Home'}) })
            }
        },
        deleteParticipantLocally (user) {
            this.participants = this.participants.filter(function (item) {
                return user.id !== item.id
            })
        },
        addParticipantLocally (user) {
            this.unenrolledStudents = this.unenrolledStudents.filter(function (item) {
                return user.id !== item.id
            })
            user.role = 'Student'
            user.group = null
            this.participants.push(user)
        },
        createGroup (group) {
            this.groups.push(group)
        },
        deleteGroup (group) {
            this.updateGroup(group)
        },
        updateGroup (group) {
            // TODO replace api function with frontend function
            groupAPI.getAllFromCourse(this.cID)
                .then(groups => { this.groups = groups })

            if (this.$hasPermission('can_view_course_users')) {
                participationAPI.getEnrolled(this.cID)
                    .then(users => { this.participants = users })
            }
        },
        updateGroups (groups) {
            this.groups = groups
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
        toggleEnrolled () {
            this.setViewEnrolled(!this.viewEnrolled)
            this.unenrolledStudents = []
            this.unenrolledQuery = ''
            this.unenrolledQueryDescription = 'Search unenrolled users in the search field above.'
        },
        deepCopyCourse (course) {
            var copyCourse = {
                name: course.name, abbreviation: course.abbreviation, startdate: course.startdate, enddate: course.enddate
            }

            return copyCourse
        },
        checkChanged () {
            if (this.course.name !== this.originalCourse.name ||
                    this.course.abbreviation !== this.originalCourse.abbreviation ||
                    this.course.startdate !== this.originalCourse.startdate ||
                    this.course.enddate !== this.originalCourse.enddate) {
                return true
            }

            return false
        },
        updateParticipants (val, uID) {
            for (var i = 0; i < this.participants.length; i++) {
                if (uID === this.participants[i].id) {
                    this.participants[i].role = val
                }
            }
            this.numTeachers = this.participants.filter(p => p.role === 'Teacher').length
        },
        searchUnenrolled () {
            this.unenrolledQuery = this.unenrolledQuery.trim()
            participationAPI.getUnenrolled(this.cID, this.unenrolledQuery)
                .then(users => {
                    this.unenrolledStudents = users
                    if (!this.unenrolledStudents.length) {
                        if (this.unenrolledQuery.length < 5) {
                            this.unenrolledQueryDescription = 'No exact match found. To search for users, give at least 5 characters.'
                        } else {
                            this.unenrolledQueryDescription = 'No users found.'
                        }
                    }
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        }
    },
    computed: {
        ...mapGetters({
            order: 'preferences/courseMembersSortAscending',
            viewEnrolled: 'preferences/courseMembersViewEnrolled',
            getCourseMembersGroupFilter: 'preferences/courseMembersGroupFilter',
            getCourseMembersSearchValue: 'preferences/courseMembersSearchValue',
            getCourseMembersSortBy: 'preferences/courseMembersSortBy'
        }),
        selectedSortOption: {
            get () {
                return this.getCourseMembersSortBy
            },
            set (value) {
                this.setCourseMembersSortBy(value)
            }
        },
        searchValue: {
            get () {
                return this.getCourseMembersSearchValue
            },
            set (value) {
                this.setCourseMembersSearchValue(value)
            }
        },
        groupFilter: {
            get () {
                return this.getCourseMembersGroupFilter
            },
            set (value) {
                this.setCourseMembersGroupFilter(value)
            }
        },
        filteredUsers () {
            let self = this

            function compareFullName (a, b) {
                return self.compare(a.full_name, b.full_name)
            }

            function compareUsername (a, b) {
                return self.compare(a.username, b.username)
            }

            function searchFilter (user) {
                var username = user.username.toLowerCase()
                var fullName = user.full_name.toLowerCase()
                var searchValue = self.getCourseMembersSearchValue.toLowerCase()

                return username.includes(searchValue) ||
                       fullName.includes(searchValue)
            }

            function groupFilter (user) {
                if (self.groupFilter) {
                    if (!user.group) {
                        return user.group === self.groupFilter
                    } else {
                        return user.group.includes(self.groupFilter)
                    }
                }

                return true
            }

            var viewList = this.participants

            /* Switch view list with drop down menu and load unenrolled
               students when accessing other students at first time. */
            if (!this.viewEnrolled) {
                viewList = this.unenrolledStudents
            }

            /* Filter list based on search input. */
            if (this.selectedSortOption === 'name') {
                viewList = viewList.sort(compareFullName)
            } else if (this.selectedSortOption === 'username') {
                viewList = viewList.sort(compareUsername)
            }

            return viewList.filter(searchFilter).filter(groupFilter)
        }
    },
    components: {
        'add-user-card': addUsersToCourseCard,
        'tooltip': tooltip,
        'bread-crumb': breadCrumb,
        'content-columns': contentColumns,
        'course-participant-card': courseParticipantCard,
        'group-editor': groupEditor,
        icon
    },
    beforeRouteLeave (to, from, next) {
        if (this.checkChanged() && !confirm('Unsaved changes will be lost if you leave. Do you wish to continue?')) {
            next(false)
            return
        }

        next()
    }
}
</script>
