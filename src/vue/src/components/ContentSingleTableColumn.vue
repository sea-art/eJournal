<template>
    <b-row no-gutters>
        <b-col cols="12" lg="8" offset-lg="2" class="main-content main-table">
            <slot/>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'ContentSingleTableColumn'
}
</script>

<style lang="sass">
.main-table
    background-color: white
</style>
