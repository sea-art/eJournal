import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Journal from '@/views/Journal'
import Assignment from '@/views/Assignment'
import Course from '@/views/Course'
import Profile from '@/views/Profile'
import Guest from '@/views/Guest'

Vue.use(Router)

export default new Router({
    routes: [{
        path: '/',
        name: 'Guest',
        component: Guest
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
        component: Course
    }, {
        path: '/Home/:course/:assign',
        name: 'Assignment',
        component: Assignment
    }, {
        path: '/Home/:course/:assign/:student',
        name: 'journal',
        component: Journal
    }]
})
