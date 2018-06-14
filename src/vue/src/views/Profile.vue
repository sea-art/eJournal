<template>
    <b-row no-gutters>
        <b-col lg="3" order="3" order-lg="1" class="left-content d-none d-lg-block"></b-col>

        <b-col md="12" lg="6" order="2" class="main-content">
            <bread-crumb :currentPage="'Settings'"></bread-crumb>

            <profile-card :name="profile[0].name"
                          :email="profile[0].email"
                          :id="profile[0].id">
                          <!-- :image="'../assets/ohno.jpeg'"> -->
                          <!-- :image="profile[0].image"> -->

                <!-- <img src="../assets/ohno.jpeg"> -->
            </profile-card>
        </b-col>

        <b-col md="12" lg="3" order="1" order-lg="3" class="right-content">
            <router-link tag="button" :to='"/Home"'>Back</router-link>
        </b-col>
    </b-row>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import profileCard from '@/components/ProfileCard.vue'

export default {
    name: 'Profile',
    data () {
        return {
            profile: [{
                name: 'Engel Hamer',
                email: 'e.hamer@uva.nl',
                id: '11256443',
                image: '../assets/ohno.jpeg'
            }]
        }
    },
    components: {
        'bread-crumb': breadCrumb,
        'profile-card': profileCard
    }
}
</script>

<style>
</style>
