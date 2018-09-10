<template>
    <b-card class="no-hover">
        <b-row>
            <b-col sm="12" lg="8" class="d-flex mb-2">
                <b-col cols="3">
                    <b>{{ groupName }}</b>
                </b-col>
            </b-col>
            <b-col sm="12" lg="4">
                <b-button v-if="$hasPermission('can_edit_course')"
                          @click.prevent.stop="removeGroup()"
                          class="delete-button full-width">
                    Remove group
                </b-button>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
import groupAPI from '@/api/group'

export default {
    props: {
        cID: {
            required: true
        },
        group: {
            required: true
        }
    },
    data () {
        return {
            groupName: ''
        }
    },
    methods: {
        removeGroup () {
            if (confirm('Are you sure you want to remove "' + this.groupName + '" from this course?')) {
                groupAPI.delete(this.cID, this.groupName).then(data => {
                    this.$toasted.success(data.description)
                    this.$emit('delete-group', this.groupName)
                }, error => {
                    this.$toasted.error(error.response.data.description)
                })
            }
        }
    },
    created () {
        this.groupName = this.group
    }
}
</script>
