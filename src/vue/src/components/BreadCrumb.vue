<template>
    <div class="bread-crumb-container">
        <b-row>
            <b-col cols="12" md="12">
                <h4></h4>
                <h1 id="h1-current-page-breadcrumb">
                    {{ currentPage }}
                    <slot>
                        <icon name="eye" @click.native="eyeClick()" class="eye-icon" scale="1.75"></icon>
                    </slot>
                </h1>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['currentPage'],
    components: {
        icon
    },
    data () {
        return {
            assignmentName: ''
        }
    },
    methods: {
        eyeClick () {
            this.$emit('eye-click')
        },
        editClick () {
            this.$emit('edit-click')
        },
        splitPath () {
            this.$router.currentRoute.path.split('/').slice(1, -1)
        }
    }
}
</script>

<style>
#h1-current-page-breadcrumb {
    margin-bottom: 0px !important;
}

/* Most paddings/margins relate to full responive build, please take care.*/
.bread-crumb {
    padding: 0px;
    background-color: var(--theme-medium-grey);
    margin-bottom: 0px;
}

.bread-crumb-container {
    padding-right: 10px;
    padding-bottom: 12px;
    margin-bottom: -4px;
}

@media(max-width:992px) {
    .bread-crumb-container  {
        padding-top: 12px !important;
        margin-top: -4px !important;
    }
}

.eye-icon {
    fill: var(--theme-light-grey) !important;
    cursor: pointer;
}

.eye-icon:hover {
    fill: var(--theme-pink) !important;
}
</style>
