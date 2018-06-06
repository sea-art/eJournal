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
         path: '/',
         name: 'Hello',
         component: Hello
       },
       {
         path: '/Courses/:name',
         name: 'courses',
         component: Courses,
         children: [
           {
             path: ':name',
             name: 'assignment',
             component: Assignment,
             children: [
               {
                   path: ':name',
                   name: 'journal',
                   component: Journal
               }
           ]
           }
         ]
       }
     ]
})
