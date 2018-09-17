import auth from '@/api/auth'

export default {

    sendFeedback (data) {
        return auth.uploadFileEmail('/send_feedback/', data)
    }
}
