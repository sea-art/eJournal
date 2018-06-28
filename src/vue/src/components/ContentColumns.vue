<template>
    <b-row no-gutters>
        <b-col lg="3" order="3" order-lg="1" class="left-content d-none d-xl-block">
            <slot name="left-content-column"></slot>
        </b-col>
        <b-col lg="12" xl="6" order="2" class="main-content">
            <slot name="main-content-column"></slot>
        </b-col>
        <b-col lg="12" xl="3" order="1" order-xl="3" class="right-content">
            <slot name="right-content-column"></slot>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'ContentColumns'
}
</script>

<style>
.left-content {
    flex: 0 0 auto;
    padding-top: 30px !important;
    padding-left: 30px !important;
    padding-right: 30px !important;
}

.main-content {
    padding-top: 40px;
    background-color: var(--theme-medium-grey);
    flex: 1 1 auto;
}

.right-content {
    flex: 0 0 auto;
    padding-top: 30px !important;
    padding-left: 30px !important;
    padding-right: 30px !important;
}

/* Needed for full responsiveness, please double check before changing!
   NOTE: max-width corresponds to bootstrap dimensions offset by 1. */
@media(max-width: 1200px){
    .right-content {
        padding: 30px !important;
    }

    .main-content {
        padding: 30px !important;
    }
}
@media (max-width: 576px) {
    .right-content {
        padding: 30px 0px !important;
    }

    .main-content {
        padding: 30px 0px !important;
    }
}
</style>
