<template>
    <div slot="main-content-column">
        <bread-crumb
            :currentPage="'Course Integration'">
        </bread-crumb>
            <p class="intro-text">You came here from a link which course is unknown.
                Do you want to create a new course on Logboek,
                or connect to an existing one?</p>
        <b-row align-h="center">
            <b-button class="button-option">
                <h2 class="button-text">Create new course</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="button-option">
                <h2 class="button-text">Connect to existing course</h2>
            </b-button>
        </b-row>
    </div>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'

export default {
    name: 'LtiCreateConnect',
    props: {
        subject: ''
    },
    components: {
        'bread-crumb': breadCrumb
    }
}
</script>

<style>
.button-option {
    width: 275px;
    height: 100px;
    margin-top: 20px;
}

.button-text {
    font-size: 20px;
    text-align: center;
}

.intro-text {
    margin-left: 15px;
    margin-right: 15px;
}
</style>
