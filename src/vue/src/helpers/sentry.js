import * as Sentry from '@sentry/browser'
import * as Integrations from '@sentry/integrations'
import store from '@/store'


function beforeSend (event, hint) { // eslint-disable-line no-unused-vars
    // Filtering can be done here https://docs.sentry.io/error-reporting/configuration/filtering/?platform=browser
    if (event.exception) {
        store.commit('sentry/SET_LAST_EVENT_ID', { eventID: event.event_id })
    }
    return event
}

export default function initSentry (Vue) {
    Sentry.init({
        dsn: CustomEnv.SENTRY_DSN,
        /* LogErrors: still call Vue's original logError function as well. */
        integrations: [new Integrations.Vue({ Vue, attachProps: true, logErrors: true })],
        beforeSend,
    })
}
