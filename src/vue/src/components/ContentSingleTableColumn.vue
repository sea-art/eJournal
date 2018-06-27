<template>
    <b-row no-gutters>
        <b-col cols="12" lg="8" offset-lg="2" class="main-table">
            <slot/>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'ContentSingleTableColumn'
}
</script>

<style>
.main-table {
    padding-top: 40px;
    flex: 1 1 auto;
}

@media(max-width:992px){
    .main-table {
        padding-top: 0px !important;
    }
}
</style>
