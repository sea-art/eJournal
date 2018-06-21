<template>
    <b-row no-gutters>
        <b-col cols="12" lg="6" offset-lg="3" class="main-content">
            <slot/>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'ContentColumns'
}
</script>

<style>
.main-content {
    padding-top: 40px;
    background-color: var(--theme-medium-grey);
    flex: 1 1 auto;
}

@media(max-width:992px){
    .main-content {
        padding-top: 0px !important;
    }
}
</style>
