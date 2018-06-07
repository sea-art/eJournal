import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Journal from '@/components/Journal'
import Assignment from '@/components/Assignment'
import Courses from '@/components/Courses'
import Login from '@/components/Login'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path : '/',
            name : 'Hello',
            component : Hello
        },
        {
            path : '/Login',
            name : 'login',
            component : Login,
        },
        {
            path : '/Courses/:course',
            name : 'courses',
            component : Courses,
        },
        {
            path : '/Courses/:course/:assign',
            name : 'assignment',
            component : Assignment,
        },
        {
            path : '/Courses/:course/:assign/:student',
            name : 'journal',
            component : Journal
        }
    ]
})
