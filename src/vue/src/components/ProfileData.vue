<template>
    <b-row>
        <b-col cols="2">
            <!-- <img src={{ image }}> -->
            <img src='../assets/ohno.jpeg'>
        </b-col>
        <b-col cols="5">
            <h7>{{ name }}</h7><br>
            <p class="profile">{{ email }}</p>
            <p class="profile">{{ id }}</p>
        </b-col>
        <b-col cols="5">TOP RIGHT</b-col>
    </b-row>
</template>

<script>
export default {
    props: ['name', 'email', 'id', 'image']
}
</script>
