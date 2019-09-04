<template>
    <b-row noGutters>
        <b-col
            lg="8"
            xl="6"
            offsetXl="3"
            class="main-content"
        >
            <slot name="main-content-column"/>
        </b-col>
        <b-col
            lg="4"
            xl="3"
            class="right-content"
        >
            <slot name="right-content-column"/>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'ContentColumns',
}
</script>
