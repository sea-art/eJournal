<template>
    <b-card class="card main-card" :class="color">
        <b-row>
            <b-col id="main-card-left-column" cols="12" lg-cols="6">
                <h2>{{ line1 }}</h2>
                {{ line2 }}
            </b-col>
            <b-col id="main-card-right-column" cols="12" lg-cols="6">
                <slot></slot>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    props: ['line1', 'line2', 'color']
}
</script>

<style>
.main-card {
    margin-bottom: 8px;
    text-align: left;
    background-color: var(--theme-light-grey);
    border-width: 0px;
    border-left-width: 20px;
    border-radius: 0px;
}
</style>
