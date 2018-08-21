<template>
    <b-card :class="$root.getBorderClass(uID)" class="no-hover">
        <div class="float-left">
            <b>{{ fullName }}</b><br>
            {{ username }}
        </div>
        <b-button v-if="this.$root.canEditCourse"
                  @click.prevent.stop="addUserToCourse()"
                  class="add-button float-right">
            <icon name="user-plus"/>
                Add
        </b-button>
    </b-card>
</template>

<script>
import courseApi from '@/api/course.js'
import icon from 'vue-awesome/components/Icon'

export default {
    props: {
        cID: {
            required: true
        },
        uID: {
            required: true
        },
        username: {
            required: true
        },
        fullName: {
            required: true
        },
        portraitPath: {
            required: true
        }
    },
    methods: {
        addUserToCourse () {
            if (confirm('Are you sure you want to add "' + this.fullName + '" to this course?')) {
                courseApi.update_course_with_student(this.uID, this.cID)
                    .then(_ => {
                        this.$emit('add-participant', 'Student',
                            this.username,
                            this.portraitPath,
                            this.uID)
                    })
                    .catch(data => {
                        this.$toasted.error(data.description)
                    })
            }
        }
    },
    components: {
        icon
    }
}
</script>
