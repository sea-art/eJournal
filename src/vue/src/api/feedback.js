import auth from '@/api/auth'

export default {

    sendFeedback (topic, type, body, browser) {
        var data = {topic: topic, type: type, body: body, browser: browser}
        return auth.post('/send_feedback/', data)
    }
}
