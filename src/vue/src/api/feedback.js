import auth from '@/api/auth'

export default {

    sendFeedback (data) {
        return auth.uploadFile('/send_feedback/', data)
    }
}
