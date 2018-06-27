<template>
    <b-card class="card" :class="color">
        <b-row>
            <b-col cols="7">
                <h6>{{ date }} {{ hours }}:{{ minutes }}</h6>
            </b-col>
            <b-col cols="5">
                <p>{{ new Date().getFullDay }}</p>
                <p v-if="this.$root.canAddCourse()">
                    {{ totalNeedsMarking }}
                </p>
            </b-col>
        </b-row>
            <h5>{{ name }}</h5>
            {{ abbr }}
    </b-card>
</template>

<script>
export default {
    props: ['date', 'hours', 'minutes', 'name', 'abbr', 'totalNeedsMarking', 'color']
}
</script>

<style scoped>
h6 {
    display: inline;
}

p {
    text-align: right;
    font-size: 20px;
    color: var(--theme-blue);
    margin-bottom: 0px;
}
</style>
