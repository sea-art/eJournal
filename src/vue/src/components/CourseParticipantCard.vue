<template>
    <b-card :class="$root.colors[uID % $root.colors.length]">
        <b-row>
            <b-col cols="4" sm="2">
                <img class="img-fluid portrait" :src="portraitPath">
            </b-col>
            <b-col cols="8" order-sm="3" sm="4">
                 <b-form-select v-model="selectedRole" class="mb-3" :select-size="1">
                    <option :selected="role === 'Student'" value="Student">Student</option>
                    <option :selected="role === 'TA'" value="TA">Teaching Assistant (TA)</option>
                    <option :selected="role === 'Teacher'" value="Teacher">Teacher</option>
                 </b-form-select>
                <b-button @click.prevent.stop="removeFromCourse()" class="delete-button full-width">Remove</b-button>
            </b-col>
            <b-col cols="12" order-sm="2" sm="6">
                {{ name }} <br/>
                {{ studentNumber }}
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    props: {
        uID: {
            required: true
        },
        studentNumber: {
            required: true
        },
        name: {
            required: true
        },
        portraitPath: {
            required: true
        },
        role: {
            required: true
        }
    },
    data () {
        return {
            selectedRole: '',
            init: true
        }
    },
    methods: {
        removeFromCourse () {
            if (confirm('Are you sure you want to remove ' + name + '?')) {
                // TODO plugin API
            }
        }
    },
    watch: {
        selectedRole: function (val) {
            if (this.init) {
                this.init = false
            } else {
                console.log(val)
            }
        }
    },
    created () {
        this.selectedRole = this.role
    }
}
</script>

<style>
</style>
