<template>
    <div class="bread-crumb-container">
        <b-row>
            <b-col cols="12" md="12">
                <h4>
                    <b-breadcrumb v-if="$route.params.student != undefined" class="bread-crumb" :items="items.concat(' ')"/>
                    <b-breadcrumb v-else-if="$route.params.assign != undefined" class="bread-crumb" :items="items.slice(0, 2).concat(' ')"/>
                    <b-breadcrumb v-else-if="$route.params.course != undefined" class="bread-crumb" :items="items.slice(0, 1).concat(' ')"/>
                </h4>
                <h1 id="h1-current-page-breadcrumb">
                    {{ currentPage }}
                    <slot>
                        <icon name="eye" @click.native="eyeClick()" class="eye-icon" scale="1.75"></icon>
                        <!-- <b-button class="float-right edit-button" @click="editClick()"> Edit </b-button> -->
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
            items: [{
                text: 'Courses',
                to: {name: 'Home'}
            }, {
                text: this.$route.params.courseName,
                to: {
                    name: 'Course',
                    params: {
                        course: this.$route.params.course,
                        courseName: this.$route.params.courseName
                    }
                }
            }, {
                text: this.$route.params.assignmentName,
                to: {
                    name: 'Assignment',
                    params: {
                        course: this.$route.params.course,
                        assign: this.$route.params.assign,
                        courseName: this.$route.params.courseName,
                        assignmentName: this.$route.params.assignmentName
                    }
                }
            // }, {
            //     text: this.assign,
            //     to: {
            //         name: 'Journal',
            //         params: {
            //             course: this.$route.params.course,
            //             assign: this.$route.params.assign,
            //             courseName: this.$route.params.courseName,
            //             assignmentName: this.$route.params.assignmentName
            //         }
            //     }
            }]
        }
    },
    methods: {
        eyeClick () {
            this.$emit('eye-click')
        },
        editClick () {
            this.$emit('edit-click')
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
    color: var(--theme-light-grey);
}

.eye-icon:hover {
    color: var(--theme-pink);
}
</style>
