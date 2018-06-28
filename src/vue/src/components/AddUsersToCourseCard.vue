<template>
    <b-card :class="$root.colors[uID % $root.colors.length]" class="no-hover">
        <b-row>
            <b-col cols="4" order-sm="2" sm="4">
                StudentID: {{ uID }}
            </b-col>
            <b-col cols="4" order-sm="2" sm="4">
                Name: {{ name }}
            </b-col>
            <b-col cols="4" order-sm="3" sm="3">
                <b-button v-if="this.$root.canEditCourse"
                          @click.prevent.stop="addUserToCourse()"
                          class="add-button full-width">
                    Add
                </b-button>
            </b-col>
        </b-row>
    </b-card></template>

<script>
import courseApi from '@/api/course.js'

export default {
    props: {
        cID: {
            required: true
        },
        uID: {
            required: true
        },
        name: {
            required: true
        },
        portraitPath: {
            required: true
        }
    },
    methods: {
        addUserToCourse () {
            if (confirm('Are you sure you want to add ' + this.name + ' to the course?')) {
                courseApi.update_course_with_studentID(this.uID, this.cID)
                    .then(response => {
                        this.$emit('add-participant', 'Student',
                            this.name,
                            this.portraitPath,
                            this.uID)
                    })
            }
        }
    }
}
</script>
