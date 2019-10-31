import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import routerConstraints from '@/utils/constants/router_constraints.js'
import Home from '@/views/Home.vue'
import Journal from '@/views/Journal.vue'
import CreateJoinJournal from '@/views/CreateJoinJournal.vue'
import Assignment from '@/views/Assignment.vue'
import Course from '@/views/Course.vue'
import Profile from '@/views/Profile.vue'
import Guest from '@/views/Guest.vue'
import Login from '@/views/Login.vue'
import PasswordRecovery from '@/views/PasswordRecovery.vue'
import Register from '@/views/Register.vue'
import LtiLaunch from '@/views/LtiLaunch.vue'
import AssignmentsOverview from '@/views/AssignmentsOverview.vue'
import ErrorPage from '@/views/ErrorPage.vue'
import NotSetup from '@/views/NotSetup.vue'
import CourseEdit from '@/views/CourseEdit.vue'
import UserRoleConfiguration from '@/views/UserRoleConfiguration.vue'
import FormatEdit from '@/views/FormatEdit.vue'
import LtiLogin from '@/views/LtiLogin.vue'
import Logout from '@/views/Logout.vue'
import EmailVerification from '@/views/EmailVerification.vue'

Vue.use(Router)

const router = new Router({
    mode: 'history',
    routes: [{
        path: '/',
        name: 'Guest',
        component: Guest,
    }, {
        path: '/Home',
        name: 'Home',
        component: Home,
    }, {
        path: '/Login',
        name: 'Login',
        component: Login,
    }, {
        path: '/PasswordRecovery/:username/:recoveryToken',
        name: 'PasswordRecovery',
        component: PasswordRecovery,
        props: true,
    }, {
        path: '/EmailVerification/:username/:token',
        name: 'EmailVerification',
        component: EmailVerification,
        props: true,
    }, {
        path: '/Register',
        name: 'Register',
        component: Register,
    }, {
        path: '/Profile',
        name: 'Profile',
        component: Profile,
    }, {
        path: '/LtiLaunch',
        name: 'LtiLaunch',
        component: LtiLaunch,
    }, {
        path: '/LtiLogin',
        name: 'LtiLogin',
        component: LtiLogin,
    }, {
        path: '/AssignmentsOverview',
        name: 'AssignmentsOverview',
        component: AssignmentsOverview,
    }, {
        path: '/Error',
        name: 'ErrorPage',
        component: ErrorPage,
        props: true,
    }, {
        path: '/NotSetup',
        name: 'NotSetup',
        component: NotSetup,
        props: true,
    }, {
        path: '/Logout',
        name: 'Logout',
        component: Logout,
    }, {
        path: '/Home/Course/:cID',
        name: 'Course',
        component: Course,
        props: true,
    }, {
        path: '/Home/Course/:cID/CourseEdit',
        name: 'CourseEdit',
        component: CourseEdit,
        props: true,
    }, {
        path: '/Home/Course/:cID/CourseEdit/UserRoleConfiguration',
        name: 'UserRoleConfiguration',
        component: UserRoleConfiguration,
        props: true,
    }, {
        path: '/Home/Course/:cID/Assignment/:aID',
        name: 'Assignment',
        component: Assignment,
        props: true,
    }, {
        path: '/Home/Course/:cID/Assignment/:aID/Format',
        name: 'FormatEdit',
        component: FormatEdit,
        props: true,
    }, {
        path: '/Home/Course/:cID/Assignment/:aID/Journal/New',
        name: 'CreateJoinJournal',
        component: CreateJoinJournal,
        props: true,
    }, {
        path: '/Home/Course/:cID/Assignment/:aID/Journal/:jID',
        name: 'Journal',
        component: Journal,
        props: true,
    }, {
        path: '*',
        name: 'NotFound',
        component: ErrorPage,
        props: {
            code: '404',
            reasonPhrase: 'Not Found',
            description: 'We\'re sorry but we can\'t find the page you tried to access.',
        },
    }],
})

router.beforeEach((to, from, next) => {
    const loggedIn = store.getters['user/loggedIn']

    if (from.name) {
        router.app.previousPage = from
    }

    if (loggedIn && routerConstraints.UNAVAILABLE_WHEN_LOGGED_IN.has(to.name)) {
        next({ name: 'Home' })
    } else if (!loggedIn && !routerConstraints.PERMISSIONLESS_CONTENT.has(to.name)) {
        store.dispatch('user/validateToken')
            .then(() => { next() })
            .catch(() => {
                router.app.previousPage = to
                next({ name: 'Login' })
            })
    } else { next() }
})

export default router
