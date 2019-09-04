<template>
    <b-row noGutters>
        <b-col
            :class="'main-content ' + extraClasses"
            lg="8"
            xl="6"
            offsetLg="2"
            offsetXl="3"
        >
            <slot/>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'ContentColumn',
    props: {
        extraClasses: {
            default: '',
        },
    },
}
</script>
