import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Journal from '@/components/Journal'
import Assignment from '@/components/Assignment'
import Courses from '@/components/Courses'
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
            path: '/Courses',
            name: 'Home',
            component: Home
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
            path: '/Courses/:course',
            name: 'courses',
            component: Courses
        },
        {
            path: '/Courses/:course/:assign',
            name: 'assignment',
            component: Assignment
        },
        {
            path: '/Courses/:course/:assign/:student',
            name: 'journal',
            component: Journal
        }
    ]
})
