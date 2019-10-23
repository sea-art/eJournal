import * as Sentry from '@sentry/browser'
import * as Integrations from '@sentry/integrations'
import store from '@/store'


function beforeSend (event, hint) { // eslint-disable-line no-unused-vars
    // Filtering can be done here https://docs.sentry.io/error-reporting/configuration/filtering/?platform=browser
    if (event.exception) {
        store.commit('sentry/SET_LAST_EVENT_ID', { eventID: event.event_id })
    }

    if (hint && hint.originalException) {
        const originalException = hint.originalException

        if (event.extra === undefined) { event.extra = {} }
        if (originalException.config) { event.extra.config = originalException.config }
        if (originalException.request) { event.extra.request = originalException.request }
        if (originalException.response) { event.extra.response = originalException.response }
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
