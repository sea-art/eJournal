<template>
    <b-card class="card main-card">
        <b-row>
            <b-col id="main-card-left-column" xs-cols="12" lg-cols="6">
                <h>{{ line1 }}</h><br/>
                <h>{{ line2 }}</h>
            </b-col>
            <b-col id="main-card-right-column" xs-cols="12" lg-cols="6">
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
</style>
