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
import LtiLogin from '@/views/LtiLogin'
import Logout from '@/views/Logout'
import authAPI from '@/api/auth.js'

Vue.use(Router)

var router = new Router({
    mode: 'history',
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
        path: '/LtiLogin',
        name: 'LtiLogin',
        component: LtiLogin
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
    router.app.previousPage = from

    /* If undefined, this means this is a hard refresh, therefore we have to call up the state. */
    if (router.app.validToken === undefined) {
        authAPI.testValidToken().catch(_ => console.error('Token not valid'))
    }

    if (to.matched.length === 0) {
        return next({name: 'ErrorPage', params: {code: '404', message: 'Page not found'}})
    }

    /* If valid token, redirect to Home, if not currently valid, look to see if it is valid.
     * If now valid, redirect as well, otherwise continue to guest page.
     */
    if (to.name === 'Guest') {
        if (router.app.validToken) {
            return next({name: 'Home'})
        } else {
            return authAPI.testValidToken()
                .then(_ => next({name: 'Home'}))
                .catch(_ => next())
        }
    } else if (['Login', 'LtiLogin', 'LtiLaunch', 'Register', 'ErrorPage'].includes(to.name)) {
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
            router.app.$toasted.error('Error while loading permissions.')
        })

    next()
})

export default router
