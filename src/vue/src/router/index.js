import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '@/components/Dashboard'
import Journal from '@/components/Journal'
import Assignment from '@/components/Assignment'
import Course from '@/components/Course'
import Login from '@/components/Login'
import Profile from '@/components/Profile'

Vue.use(Router)

export default new Router({
    /* the router controls the path and which component is used in the
     * router-view
     */
    routes: [
        {
            path: '/',
            name: 'Login',
            component: Login
        },
        {
            path: '/Course',
            name: 'Dashboard',
            component: Dashboard
        },
        {
            path: '/Profile',
            name: 'Profile',
            component: Profile
        },
        {
            /* In the courses path the sub paths are variable so each
             * assignment, course and journal has his own link but use the same
             * router view.
             */
            path: '/Course/:course',
            name: 'course',
            component: Course
        },
        {
            path: '/Course/:course/:assign',
            name: 'assignment',
            component: Assignment
        },
        {
            path: '/Course/:course/:assign/:student',
            name: 'journal',
            component: Journal
        }
    ]
})
