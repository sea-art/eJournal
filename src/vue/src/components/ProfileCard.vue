<template>
    <b-card class="profile-card">
        <profile-data :name="name"
                      :email="email"
                      :id="id">
                      <!-- :image="image"> -->
        </profile-data>

        <notification-card></notification-card>
        <password-card></password-card>
    </b-card>
</template>

<script>
import profileData from '@/components/ProfileData.vue'
import notificationCard from '@/components/NotificationCard.vue'
import passwordCard from '@/components/PasswordCard.vue'

export default {
    props: ['name', 'email', 'id', 'image'],
    components: {
        'profile-data': profileData,
        'notification-card': notificationCard,
        'password-card': passwordCard
    }
}
</script>

<style>
.profile-card {
    margin-top: 12px;
    text-align: left;
    background-color: var(--theme-light-grey);
    border-width: 0px;
    border-left-width: 20px;
    border-radius: 0px;
    border-left-color: var(--theme-blue);
}

h7 {
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 0px;
}

h8 {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 0px;
}
p.profile-data {
    font-size: 15px;
    line-height: 10px;
    margin-bottom: 10px;
}

p.profile-notification {
    font-size: 20px;
    line-height: 15px;
    margin-bottom: 28px;
}

p.profile-password {
    font-size: 20px;
    line-height: 15px;
    margin-bottom: 28px;
}
</style>
