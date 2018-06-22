<template>
    <content-single-column>
        <bread-crumb @eye-click="customisePage">&nbsp;</bread-crumb>
        <b-card class="no-hover">
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
                         v-model="course.date"
                         type="date"
                         required/>

                <b-row>
                    <b-col lg="2" md="5">
                        <b-button class="add-button" type="submit">Update Course</b-button>
                    </b-col>
                    <b-col lg="2" md="5">
                        <b-button @click.prevent.stop="deleteCourse()" class="delete-button">Delete Course</b-button>
                    </b-col>
                    <b-col lg="3" md="3">
                        <b-form-select v-model="selectedSortOption" :select-size="1">
                           <option :value="null">Sort on ...</option>
                           <option value="sortName">Sort on name</option>
                           <option value="sortID">Sort on ID</option>
                        </b-form-select>
                    </b-col>
                </b-row>
            </b-form>
        </b-card>

        <!-- TODO PROVIDE FULL NAME AND STUDENTNUMBER DATABASE BOYS -->
        <course-participant-card v-for="p in participants" :key="p.uID"
            :cID="cID"
            :uID="p.uID"
            :studentNumber="p.studentNumber"
            :name="p.name"
            :portraitPath="p.picture"
            :role="p.role"/>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
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
            selectedSortOption: null
        }
    },
    created () {
        courseApi.get_course_data(this.cID)
            .then(response => {
                this.course = response
            })
            .catch(_ => alert('Error while loading course data'))

        courseApi.get_users(this.cID)
            .then(response => {
                this.participants = response.users
            })
            .catch(_ => alert('Error while loading course users'))
    },
    methods: {
        onSubmit () {
            courseApi.update_course(this.cID,
                this.course.name,
                this.course.abbr,
                this.course.date)
                .then(response => {
                    this.course = response
                    console.log(this.course.date)
                    this.pageName = this.course.name
                })
        },
        deleteCourse () {
            if (confirm('Are you sure you want to delete ' + this.course.name + '?')) {
                courseApi.delete_course(this.cID)
                    .then(response => {
                        this.$router.push({name: 'Home'})
                    })
            }
        }
    },
    watch: {
        selectedSortOption: function (val) {
            if (this.init) {
                this.init = false
            } else {
                this.selectedSortOption = val
                if (val === 'sortName') {
                    this.participants = this.participants.sort((a, b) => a.name > b.name)
                } else if (val === 'sortID') {
                    this.participants = this.participants.sort((a, b) => a.uID > b.uID)
                }
                console.log(this.participants)
            }
        }
    },
    components: {
        'content-single-column': contentSingleColumn,
        'course-participant-card': courseParticipantCard,
        'bread-crumb': breadCrumb
    }
}
</script>

<style>
#pushBot {
    margin-bottom: 10px;
}
</style>
