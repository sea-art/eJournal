import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Journal from '@/views/Journal'
import Assignment from '@/views/Assignment'
import Course from '@/views/Course'
import Profile from '@/views/Profile'
import Guest from '@/views/Guest'
import Register from '@/views/Register'
import LtiLaunch from '@/views/LtiLaunch'

Vue.use(Router)

export default new Router({
    routes: [{
        path: '/',
        name: 'Guest',
        component: Guest
    }, {
        path: '/Register',
        name: Register,
        component: Register
    }, {
        path: '/Home',
        name: 'Home',
        component: Home
    }, {
        path: '/Profile',
        name: 'Profile',
        component: Profile
    }, {
        path: '/Home/:course',
        name: 'Course',
        component: Course,
        props: {
            courseName: '',
            color: ''
        }
    }, {
        path: '/Home/:course/:assign',
        name: 'Assignment',
        component: Assignment,
        props: {
            color: '',
            courseName: '',
            assignmentName: ''
        }
    }, {
        path: '/Home/:course/:assign/:student',
        name: 'Journal',
        component: Journal,
        props: {
            color: '',
            courseName: '',
            assignmentName: '',
            journalName: ''
        }
    }, {
        path: '/lti/launch',
        name: 'LtiLaunch',
        component: LtiLaunch
    }]
})
