<template>
    <b-row noGutters>
        <b-col
            cols="12"
            lg="8"
            offsetLg="2"
            class="main-content main-table"
        >
            <slot/>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'ContentSingleTableColumn',
}
</script>
