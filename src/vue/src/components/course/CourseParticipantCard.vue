<template>
    <b-card :class="$root.getBorderClass(uID)" class="no-hover">
        <b-row>
            <b-col sm="12" lg="8" class="d-flex mb-2">
                <b-col cols="3" class="text-center">
                    <img class="profile-picture" :src="portraitPath">
                </b-col>
                <b-col cols="9">
                    <b>{{ fullName }}</b> ({{ selectedRole }})<br/>
                    {{ username }}
                </b-col>
            </b-col>
            <b-col sm="12" lg="4">
                <div class="shadow">
                    <b-form-select v-if="$hasPermission('can_edit_course_roles')"
                                   v-model="selectedRole"
                                   :select-size="1">
                        <option v-for="r in roles" :key="r.name" :value="r.name">
                            {{r.name}}
                        </option>
                    </b-form-select>
                </div>
                <!-- TODO Permission revision should be can_delete_course_users -->
                <b-button v-if="$hasPermission('can_add_course_participants')"
                          @click.prevent.stop="removeFromCourse()"
                          class="delete-button full-width">
                    <icon name="user-times"/>
                    Remove
                </b-button>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
import courseApi from '@/api/course.js'
import permissions from '@/api/permissions.js'
import icon from 'vue-awesome/components/Icon'

export default {
    props: {
        cID: {
            required: true
        },
        uID: {
            required: true
        },
        index: {
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
        },
        role: {
            required: true
        }
    },
    data () {
        return {
            selectedRole: '',
            init: true,
            roles: []
        }
    },
    methods: {
        removeFromCourse () {
            if (confirm('Are you sure you want to remove "' + this.fullName + '" from this course?')) {
                courseApi.delete_user_from_course(this.uID, this.cID).then(data => {
                    this.$toasted.success(data.description)
                    if (this.$store.getters['user/uID'] === this.uID) {
                        this.$store.dispatch('user/populateStore').catch(_ => {
                            this.$toasted.error('The website might be out of sync, please login again.')
                        })
                        this.$router.push({name: 'Home'})
                    }
                    this.$emit('delete-participant', this.role,
                        this.username,
                        this.portraitPath,
                        this.uID)
                }, error => {
                    this.$toasted.error(error.response.data.description)
                })
            }
        }
    },
    watch: {
        selectedRole: function (val) {
            if (this.init) {
                this.init = false
            } else {
                this.selectedRole = val
                this.$emit('update:role', val)
                courseApi.update_user_role_course(this.uID, this.cID, this.selectedRole).then(_ => {
                    if (this.$store.getters['user/uID'] === this.uID) {
                        this.$store.dispatch('user/populateStore').then(_ => {
                            this.$router.push({name: 'Course', params: {cID: this.cID}})
                        }, _ => {
                            this.$toasted.error('The website might be out of sync, please login again.')
                        })
                    }
                }, error => {
                    this.$toasted.error(error.response.data.description)
                })
            }
        }
    },
    created () {
        this.selectedRole = this.role

        permissions.get_course_roles(this.cID)
            .then(roles => {
                this.roles = roles
            })
            .catch(error => { this.$toasted.error(error.response.data.description) })
    },
    components: {
        icon
    }
}
</script>
