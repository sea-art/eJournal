<template>
    <b-card :class="$root.getBorderClass(uID)" class="no-hover">
        <div class="float-left">
            <b>{{ name }}</b><br>
            {{ uID }}
        </div>
        <b-button v-if="this.$root.canEditCourse"
                  @click.prevent.stop="addUserToCourse()"
                  class="add-button float-right">
                    Add
        </b-button>
    </b-card>
</template>

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
                courseApi.update_course_with_student(this.uID, this.cID)
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
