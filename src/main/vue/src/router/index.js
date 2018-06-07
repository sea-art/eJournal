import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Journal from '@/components/Journal'
import Assignment from '@/components/Assignment'
import Courses from '@/components/Courses'
import Login from '@/components/Login'
import Profile from '@/components/Profile'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Login',
            component: Login
        },
        {
            path: '/Courses',
            name: 'Hello',
            component: Hello
        },
        {
            path: '/Profile',
            name: 'Profile',
            component: Profile
        },
        {
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
