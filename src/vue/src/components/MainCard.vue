<template>
    <b-card id="card" class="main-card" :class="color" @mouseover="hover">
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

.main-card.pink-border {
    border-left-color: var(--theme-pink);
}

.main-card.peach-border {
    border-left-color: var(--theme-peach);
}

.main-card.blue-border {
    border-left-color: var(--theme-blue);
}

.main-card:hover {
    background-color: var(--theme-dark-grey);
}
</style>
