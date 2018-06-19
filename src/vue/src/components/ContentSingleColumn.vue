<template>
    <b-row no-gutters>
        <b-col lg="3" order="3" order-lg="1" class="left-content d-none d-lg-block">
            <slot name="left-content-column"></slot>
        </b-col>
        <b-col md="12" lg="6" order="2" class="main-content">
            <slot name="main-content-column"></slot>
        </b-col>
        <b-col md="12" lg="3" order="1" order-lg="3" class="right-content d-none d-lg-block">
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

/* Needed for full responsiveness, please double check before changing! */
@media(max-width:992px){
    .right-content {
        padding: 0px !important;
        margin-top: 8px;
    }

    .main-content {
        padding-top: 0px !important;
    }
}
@media(min-width:768px){}
@media(min-width:992px){}
@media(min-width:1200px){}
</style>
