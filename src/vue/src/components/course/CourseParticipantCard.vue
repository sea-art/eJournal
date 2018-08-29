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
                    <b-form-select v-if="this.$root.canEditCourseRoles"
                                   v-model="selectedRole"
                                   :select-size="1">
                        <option v-for="r in roles" :key="r.name" :value="r.name">
                            {{ r.name }}
                        </option>
                    </b-form-select>
                </div>
                <b-button v-if="this.$root.canEditCourse"
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
import commonAPI from '@/api/common'

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
            if (confirm('Are you sure you want to remove "' + this.fullName + '" from this course?')) {
                participationAPI.delete(this.cID, this.uID)
                    .then(data => {
                        this.$toasted.success(data.description)
                        this.$emit('delete-participant', this.role,
                            this.username,
                            this.portraitPath,
                            this.uID)
                    })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        },
        checkPermission () {
            commonAPI.getPermissions(this.cID)
                .then(permissions => {
                    this.$root.generalPermissions = permissions
                    if (!this.$root.canEditCourse()) {
                        this.$router.push({
                            name: 'Home'
                        })
                    }
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        }
    },
    watch: {
        selectedRole (val) {
            if (this.init) {
                this.init = false
            } else {
                this.selectedRole = val
                this.$emit('update:role', val)
                participationAPI.update(this.cID, {user_id: this.uID, role: this.selectedRole})
                    .then(_ => {
                        this.checkPermission()
                    })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        }
    },
    created () {
        this.selectedRole = this.role
    },
    components: {
        icon
    }
}
</script>
