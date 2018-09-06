<template>
    <b-card :class="$root.getBorderClass(user.id)" class="no-hover">
        <b-row>
            <b-col sm="12" lg="8" class="d-flex mb-2">
                <b-col cols="3" class="text-center">
                    <img class="profile-picture" :src="user.profile_picture">
                </b-col>
                <b-col cols="9">
                    <b>{{ user.name }}</b> ({{ user.role }})<br/>
                    {{ user.username }}
                </b-col>
            </b-col>
            <b-col sm="12" lg="4">
                <div class="shadow">
                    <b-form-select v-if="$hasPermission('can_edit_course_roles')"
                                   v-model="selectedRole"
                                   :select-size="1">
                        <option v-for="r in roles" :key="r.name" :value="r.name">
                            {{ r.name }}
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
import icon from 'vue-awesome/components/Icon'

import participationAPI from '@/api/participation'

export default {
    props: {
        cID: {
            required: true
        },
        user: {
            required: true
        },
        roles: {
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
            if (confirm('Are you sure you want to remove "' + this.user.name + '" from this course?')) {
                participationAPI.delete(this.cID, this.user.id).then(data => {
                    this.$toasted.success(data.description)
                    if (this.$store.getters['user/uID'] === this.user.id) {
                        this.$store.dispatch('user/populateStore').catch(_ => {
                            this.$toasted.error('The website might be out of sync, please login again.')
                        })
                        this.$router.push({name: 'Home'})
                    }
                    this.$emit('delete-participant', this.user)
                }, error => {
                    this.$toasted.error(error.response.data.description)
                })
            }
        }
    },
    watch: {
        selectedRole (val) {
            if (this.init) {
                this.init = false
            } else {
                this.selectedRole = val
                this.user.role = val
                participationAPI.update(this.cID, {user_id: this.user.id, role: this.selectedRole}).then(_ => {
                    if (this.$store.getters['user/uID'] === this.user.id) {
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
        this.selectedRole = this.user.role
    },
    components: {
        icon
    }
}
</script>
