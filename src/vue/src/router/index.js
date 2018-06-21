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
import AssignmentsOverview from '@/views/AssignmentsOverview'
import permissionsApi from '@/api/permissions.js'
import ErrorPage from '@/views/ErrorPage'
// import CourseEdit from '@/views/CourseEdit'
import AssignmentEdit from '@/views/AssignmentEdit'

Vue.use(Router)

var router = new Router({
    routes: [{
        path: '/',
        name: 'Guest',
        component: Guest
    }, {
        path: '/Home',
        name: 'Home',
        component: Home
    }, {
        path: '/Register',
        name: Register,
        component: Register
    }, {
        path: '/Profile',
        name: 'Profile',
        component: Profile
    }, {
        path: '/AssignmentsOverview',
        name: 'AssignmentsOverview',
        component: AssignmentsOverview
    }, {
        path: '/ErrorPage',
        name: 'ErrorPage',
        component: ErrorPage
    }, {
        path: '/Home/Course/:cID',
        name: 'Course',
        component: Course,
        props: true
    }, {
        path: '/Home/Course/:cID/Assignment/:aID',
        name: 'Assignment',
        component: Assignment,
        props: true
    }, {
        path: '/Home/Course/:cID/Assignment/:aID/AssignmentEdit',
        name: 'AssignmentEdit',
        component: AssignmentEdit,
        props: true
    }, {
        path: '/Home/Course/:cID/Assignment:aID/Journal/:jID',
        name: 'Journal',
        component: Journal,
        props: true
    }, {
        path: '/lti/launch',
        name: 'LtiLaunch',
        component: LtiLaunch
    }]
})

router.beforeEach((to, from, next) => {
    // TODO Possible redirect if token invalid?
    // TODO Handle errors properly
    // TODO Caching for permisisons, how to handle permission changes when role is altered by teacher

    var params
    if (to.params.cID) {
        params = to.params.cID
    } else {
        /* The -1 paramater queries if the user has admin priveleges */
        params = -1
    }

    permissionsApi.get_course_permissions(params)
        .then(response => {
            router.app.permissions = response
            next()
        })
        .catch(_ => {
            // TODO Check if this catch works as expected
            console.log('Error while loading permissions, does the redirect work?')
            next(vm => {
                vm.$router.push({name: 'ErrorPage', params: {errorMessage: 'Error while loading permissions', errorCode: '???'}})
            })
        })

    next()
})

export default router
