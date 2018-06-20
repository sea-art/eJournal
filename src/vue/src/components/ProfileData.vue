<template>
    <b-row>
        <b-col lg="4" md="12">
            <img :src='image'>
        </b-col>
        <b-col lg="8" md="12">
            <p class="profile-name">{{ name }}</p>
            <p class="profile-data">{{ id }}</p>
        </b-col>
    </b-row>
</template>

<script>
export default {
    props: ['name', 'id', 'image']
}
</script>
