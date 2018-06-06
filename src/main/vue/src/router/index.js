import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Journal from '@/components/Journal'
import Assignment from '@/components/Assignment'
import Courses from '@/components/Courses'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path : '/',
            name : 'Hello',
            component : Hello
        },
        {
            path : '/:course',
            name : 'courses',
            component : Courses,
        },
        {
            path : '/:course/:assign',
            name : 'assignment',
            component : Assignment,
        },
        {
            path : '/:course/:assign/:student',
            name : 'journal',
            component : Journal
        }
    ]
})
