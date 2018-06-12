<template>
    <b-card class="main-card" @mouseover="hover">
        <b-row>
            <b-col id="main-card-left-column" cols="6">
                <h2>{{ line1 }}</h2>
                {{ line2 }}
            </b-col>
            <b-col id="main-card-right-column" cols="6">
                <slot></slot>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    props: ['line1', 'line2']
}
</script>

<style>
.main-card {
    margin-bottom: 8px;
    text-align: left;
    background-color: var(--theme-light-grey);
    border-width: 0px;
    border-left-width: 20px;
    border-left-color: red;
    border-radius: 0px;
}

.main-card:hover {
    background-color: var(--theme-dark-grey);
}
</style>
