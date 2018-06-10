import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '@/views/Dashboard'
import Journal from '@/views/Journal'
import Assignment from '@/views/Assignment'
import Course from '@/views/Course'
import Login from '@/views/Login'
import Profile from '@/views/Profile'

Vue.use(Router)

export default new Router({
    /* the router controls the path and which component is used in the
     * router-view
     */
    routes: [
        {
            path: '/',
            // name: 'Login',
            component: Login
        },
        {
            path: '/Dashboard',
            // name: 'Dashboard',
            component: Dashboard
        },
        {
            path: '/Profile',
            // name: 'Profile',
            component: Profile
        },
        {
            /* In the courses path the sub paths are variable so each
             * assignment, course and journal has his own link but use the same
             * router view.
             */
            path: '/Dashboard/:course',
            name: 'Course',
            component: Course
        },
        {
            path: '/Dashboard/:course/:assign',
            // name: 'assignment',
            component: Assignment
        },
        {
            path: '/Dashboard/:course/:assign/:student',
            // name: 'journal',
            component: Journal
        }
    ]
})
