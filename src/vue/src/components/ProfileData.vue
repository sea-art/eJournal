<template>
    <b-row>
        <b-col lg="4" md="12">
            <img src='../assets/unknown-profile.png'>
        </b-col>
        <b-col lg="8" md="12">
            <p class="profile-name">{{ name }}</p>
            <p class="profile-data">{{ email }}</p>
            <p class="profile-data">{{ id }}</p>
            <p class="profile-data">{{ courses[0].name }}</p>
        </b-col>
    </b-row>
</template>

<script>
export default {
    props: ['name', 'email', 'id', 'image'],
    data () {
        return {
            courses: [{name: '1'}],
            test: 'hoi'
        }
    }
}
</script>
