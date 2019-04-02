<template>
<div>
  <h4 class="mb-2"><span>Manage course members</span></h4>
  <div class="d-flex">
    <input v-if="viewEnrolled" class="theme-input flex-grow-1 no-width multi-form mr-2" type="text" v-model="searchValue" placeholder="Search..." />
    <input v-if="!viewEnrolled" class="theme-input flex-grow-1 no-width multi-form mr-2" type="text" v-model="unenrolledQuery" placeholder="Name or username with at least 5 characters" @keyup.enter="searchUnenrolled" />
    <b-button v-if="!viewEnrolled" class="multi-form mr-2" @click="searchUnenrolled">
      <icon name="search" />
      Search users
    </b-button>
    <b-button v-if="viewEnrolled" v-on:click.stop @click="toggleEnrolled" class="multi-form">
      <icon name="users" />
      Enrolled
    </b-button>
    <b-button v-if="!viewEnrolled" v-on:click.stop @click="toggleEnrolled" class="multi-form">
      <icon name="user-plus" />
      Unenrolled
    </b-button>
  </div>
  <div class="d-flex">
    <b-form-select class="multi-form mr-2" v-model="selectedSortOption" :select-size="1">
      <option value="name">Sort by name</option>
      <option value="username">Sort by username</option>
    </b-form-select>
    <b-form-select class="multi-form mr-2" v-model="groupFilter" :select-size="1">
      <option :value="null">Filter on group...</option>
      <option v-for="group in groups" :key="group.name" :value="group.name">
        {{ group.name }}
      </option>
    </b-form-select>
    <b-button v-on:click.stop v-if="!order" @click="setOrder(!order)" class="multi-form">
      <icon name="long-arrow-down" />
      Ascending
    </b-button>
    <b-button v-on:click.stop v-if="order" @click="setOrder(!order)" class="multi-form">
      <icon name="long-arrow-up" />
      Descending
    </b-button>
  </div>
  <b-card class="no-hover" v-if="!viewEnrolled && !this.unenrolledStudents.length">
    <div class="float-left">
      <b>{{ unenrolledQueryDescription }}</b>
    </div>
  </b-card>

  <course-participant-card v-if="viewEnrolled" @delete-participant="deleteParticipantLocally" @update-participants="updateParticipants" v-for="p in filteredUsers" :key="p.id" :cID="course.id" :group.sync="p.group" :groups="groups" :user="p" :numTeachers="numTeachers"
      :roles="roles" />

  <add-user-card v-if="!viewEnrolled" @add-participant="addParticipantLocally" v-for="p in filteredUsers" :key="p.id" :cID="course.id" :user="p" />
</div>
</template>

<script>
import addUsersToCourseCard from '@/components/course/AddUsersToCourseCard.vue'
import courseParticipantCard from '@/components/course/CourseParticipantCard.vue'
import tooltip from '@/components/assets/Tooltip.vue'
import icon from 'vue-awesome/components/Icon'

import participationAPI from '@/api/participation'
import roleAPI from '@/api/role'
import groupAPI from '@/api/group'

import { mapGetters, mapMutations } from 'vuex'

export default {
    name: 'CourseEdit',
    props: {
        course: {
            required: true
        }
    },
    data () {
        return {
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
        participationAPI.getEnrolled(this.course.id)
            .then(users => { this.participants = users })
        roleAPI.getFromCourse(this.course.id)
            .then(roles => { this.roles = roles })
        groupAPI.getAllFromCourse(this.course.id)
            .then(groups => { this.groups = groups })
    },
    components: {
        'add-user-card': addUsersToCourseCard,
        'course-participant-card': courseParticipantCard,
        tooltip,
        icon
    },
    methods: {
        ...mapMutations({
            setOrder: 'preferences/SET_COURSE_MEMBERS_SORT_ASCENDING',
            setViewEnrolled: 'preferences/SET_COURSE_MEMBERS_VIEW_ENROLLED',
            setCourseMembersGroupFilter: 'preferences/SET_COURSE_MEMBERS_GROUP_FILTER',
            setCourseMembersSearchValue: 'preferences/SET_COURSE_MEMBERS_SEARCH_VALUE',
            setCourseMembersSortBy: 'preferences/SET_COURSE_MEMBERS_SORT_BY'
        }),
        compare (a, b) {
            if (a < b) { return this.order ? 1 : -1 }
            if (a > b) { return this.order ? -1 : 1 }
            return 0
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

        updateParticipants (val, uID) {
            for (var i = 0; i < this.participants.length; i++) {
                if (uID === this.participants[i].id) {
                    this.participants[i].role = val
                }
            }
            this.numTeachers = this.participants.filter(p => p.role === 'Teacher').length
        },

        toggleEnrolled () {
            this.setViewEnrolled(!this.viewEnrolled)
            this.unenrolledStudents = []
            this.unenrolledQuery = ''
            this.unenrolledQueryDescription = 'Search unenrolled users in the search field above.'
        },

        searchUnenrolled () {
            this.unenrolledQuery = this.unenrolledQuery.trim()
            participationAPI.getUnenrolled(this.course.id, this.unenrolledQuery)
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
                    return user.groups.map(group => group['name']).includes(self.groupFilter)
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
    }
}
</script>
