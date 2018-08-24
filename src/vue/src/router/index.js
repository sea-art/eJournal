import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Journal from '@/views/Journal'
import Assignment from '@/views/Assignment'
import Course from '@/views/Course'
import Profile from '@/views/Profile'
import Guest from '@/views/Guest'
import Login from '@/views/Login'
import PasswordRecovery from '@/views/PasswordRecovery'
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
import EmailVerification from '@/views/EmailVerification'

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
        path: '/PasswordRecovery/:username/:recoveryToken',
        name: 'PasswordRecovery',
        component: PasswordRecovery,
        props: true
    }, {
        path: '/EmailVerification/:token',
        name: 'EmailVerification',
        component: EmailVerification,
        props: true
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
    }, {
        path: '*',
        name: 'ErrorPage',
        component: ErrorPage,
        props: { code: '404', reasonPhrase: 'Not Found', description: `We're sorry but we can't find the page you tried to access.`}
    }]
})

const permissionlessContent = new Set([
    'Login',
    'LtiLogin',
    'LtiLaunch',
    'Register',
    'ErrorPage',
    'PasswordRecovery',
    'EmailVerification',
    'Guest'
])

const unavailableWhenLoggedIn = new Set([
    'Guest',
    'Register'
])

router.beforeEach((to, from, next) => {
    // TODO Caching for permissions, how to handle permission changes when role is altered by teacher
    router.app.previousPage = from

    /* If undefined, this means this is a hard refresh, therefore we have to call up the state. */
    if (router.app.validToken === undefined) {
        authAPI.testValidToken().catch(_ => console.error('Token not valid'))
    }

    /* If valid token, redirect to Home, if not currently valid, look to see if it is valid.
     * If now valid, redirect as well, otherwise continue to guest page.
     */
    if (unavailableWhenLoggedIn.has(to.name)) {
        if (router.app.validToken) {
            return next({name: 'Home'})
        } else {
            return authAPI.testValidToken()
                .then(_ => next({name: 'Home'}))
                .catch(_ => next())
        }
    } else if (permissionlessContent.has(to.name)) {
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
            router.app.generalPermissions = response

            if (to.params.aID) {
                permissionsApi.get_assignment_permissions(to.params.aID)
                    .then(response => {
                        router.app.assignmentPermissions = response
                        return next()
                    })
                    .catch(_ => {
                        router.app.$toasted.error('Error while loading assignment permissions.')
                    })
            } else {
                return next()
            }
        })
        .catch(_ => {
            router.app.$toasted.error('Error while loading course permissions.')
        })
})

export default router
