import * as types from '../constants/permission-types.js'
import router from '@/router'

const getters = {
    hasPermission: (state, getters, rootState, rootGetters) => (permission, givenKeyLevel = null, id = null) => {
        if (!rootGetters['user/loggedIn']) { return false }
        if ((!types.ALL_PERIMSSIONS.has(permission))) { throw Error('Permission input error, the requested permission does not exist.') }
        if (givenKeyLevel && !types.PERMISSION_KEY_LEVELS.has(givenKeyLevel)) { throw Error('Permission input error, the requested key level does not exist.') }
        if (givenKeyLevel === 'general' && id) { throw Error('Permission input error, general permissions are without id.') }

        const permissions = rootGetters['user/permissions']
        const routeParams = router.currentRoute.params

        if ('cID' in routeParams) {
            return permissions[givenKeyLevel || 'course' + routeParams.cID][permission]
        } else if ('aID' in routeParams) {
            return permissions[givenKeyLevel || 'assignment' + routeParams.aID][permission]
        } else {
            return permissions[givenKeyLevel || 'general'][permission]
        }
    }
}

export default {
    namespaced: true,
    getters
}
