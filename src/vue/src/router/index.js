import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Journal from '@/views/Journal'
import Assignment from '@/views/Assignment'
import Course from '@/views/Course'
import Profile from '@/views/Profile'
import Guest from '@/views/Guest'
import Login from '@/views/Login'
import Register from '@/views/Register'
import LtiLaunch from '@/views/LtiLaunch'
import AssignmentsOverview from '@/views/AssignmentsOverview'
import permissionsApi from '@/api/permissions.js'
import ErrorPage from '@/views/ErrorPage'
import CourseEdit from '@/views/CourseEdit'
import AssignmentEdit from '@/views/AssignmentEdit'
import UserRoleConfiguration from '@/views/UserRoleConfiguration'
import FormatEdit from '@/views/FormatEdit'
import Logout from '@/views/Logout'
import authAPI from '@/api/auth.js'

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
        path: '/Login',
        name: 'Login',
        component: Login
    }, {
        path: '/Register',
        name: 'Register',
        component: Register
    }, {
        path: '/Profile',
        name: 'Profile',
        component: Profile
    }, {
        path: '/LtiLaunch',
        name: 'LtiLaunch',
        component: LtiLaunch
    }, {
        path: '/AssignmentsOverview',
        name: 'AssignmentsOverview',
        component: AssignmentsOverview
    }, {
        path: '/Error',
        name: 'ErrorPage',
        component: ErrorPage,
        props: true
    }, {
        path: '/Logout',
        name: 'Logout',
        component: Logout
    }, {
        path: '/Home/Course/:cID',
        name: 'Course',
        component: Course,
        props: true
    }, {
        path: '/Home/Course/:cID/CourseEdit',
        name: 'CourseEdit',
        component: CourseEdit,
        props: true
    }, {
        path: '/Home/Course/:cID/CourseEdit/UserRoleConfiguration',
        name: 'UserRoleConfiguration',
        component: UserRoleConfiguration,
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
        path: '/Home/Course/:cID/Assignment/:aID/Format',
        name: 'FormatEdit',
        component: FormatEdit,
        props: true
    }, {
        path: '/Home/Course/:cID/Assignment/:aID/Journal/:jID',
        name: 'Journal',
        component: Journal,
        props: true
    }]
})

router.beforeEach((to, from, next) => {
    // TODO Caching for permissions, how to handle permission changes when role is altered by teacher

    console.log('Before each to:')
    console.log(to)
    // console.log(from)

    if (!router.app.validToken) {
        authAPI.testValidToken()
    }

    if (to.matched.length === 0) {
        console.log('Before each: No match detected rerouting to 404')
        return next({name: 'ErrorPage', params: {code: '404', message: 'Page not found'}})
    }

    /* Returning next because we short circuit the function here, no API calls
    * are desired. */
    if (to.name === 'Guest') {
        return next()
    } else if (to.name === 'Login') {
        console.log(from.name)
        router.app.previousPage = from
        return next()
    }

    var params
    if (to.params.cID) {
        params = to.params.cID
    } else {
        /* -1 is used to indicate that the course ID (cID) is not known. This
        is used for sitewide permissions. */
        params = -1
    }

    permissionsApi.get_course_permissions(params)
        .then(response => {
            router.app.permissions = response
        })
        .catch(_ => {
            // TODO Check if this catch works as expected
            console.log('Error while loading permissions, does the redirect work?')
            // next(vm => {
            // vm.$router.push({name: 'ErrorPage', params: {errorMessage: 'Error while loading permissions', errorCode: '401'}})
            // })
        })

    next()
})

export default router
