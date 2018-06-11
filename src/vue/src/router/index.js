import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
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
        {path: '/', component: Login},
        {path: '/Home', component: Home
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
            path: '/Home/:course',
            name: 'Course',
            component: Course
        },
        {
            path: '/Home/:course/:assign',
            // name: 'assignment',
            component: Assignment
        },
        {
            path: '/Home/:course/:assign/:student',
            // name: 'journal',
            component: Journal
        }
    ]
})
