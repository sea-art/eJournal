<template>
    <b-row v-if="windowWidth > 750" no-gutters>
        <b-col cols="12" lg="6" offset-lg="3" class="table-content">
            <bread-crumb>&nbsp;</bread-crumb>
            <div class="light-text">
                <table class="table table-bordered table-hover">
                    <thead >
                        <tr>
                            <th/>
                            <th v-for="role in roles" :key="'th-' + role">{{ role }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="permission in permissions" :key="permission">
                            <td>{{ permission }}</td>
                            <td v-for="role in roles" :key="role + '-' + permission">
                                <custom-checkbox
                                @checkbox-toggle="updateRole"
                                :role="role"
                                :permission="permission"
                                :receivedState="false"/>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </b-col>
    </b-row>
    <b-row v-else no-gutters>
        <b-col cols="12" lg="6" offset-lg="3" class="table-content">
            <bread-crumb>&nbsp;</bread-crumb>
            <div class="light-text">
                <table class="table table-bordered table-hover">
                    <thead >
                        <tr>
                            <th/>
                            <b-form-select
                                class="select-center mb-3"
                                v-model="selectedRole"
                                :options="selectRoles"/>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="permission in permissions" :key="permission">
                            <td>{{ permission }}</td>
                            <td>
                                <custom-checkbox
                                @checkbox-toggle="updateRole"
                                :role="selectedRole"
                                :permission="permission"
                                :receivedState="false"/>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </b-col>
    </b-row>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import customCheckbox from '@/components/CustomCheckbox.vue'

export default {
    name: 'UserRoleConfiguration',
    props: {
        cID: {
            required: true
        }
    },
    data () {
        return {
            roles: [
                'Student',
                'TA',
                'Teacher',
                'Admin',
                'Observer'
            ],
            selectRoles: [
                {value: null, text: 'Please select a role'},
                {value: 'Student', text: 'Student'},
                {value: 'TA', text: 'TA'},
                {value: 'Admin', text: 'Admin'},
                {value: 'Observer', text: 'Observer'},
                {}
            ],
            permissions: ['Can edit course', 'Can add course'],
            selectedRole: null,
            windowWidth: 550
        }
    },
    methods: {
        getWindowWidth (event) {
            this.windowWidth = document.documentElement.clientWidth
        },
        updateRole (list) {
            console.log(list)
        }
    },
    mounted () {
        this.$nextTick(function () {
            window.addEventListener('resize', this.getWindowWidth)

            this.getWindowWidth()
        })
    },
    beforeDestroy () {
        window.removeEventListener('resize', this.getWindowWidth)
    },
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb,
        'custom-checkbox': customCheckbox
    }
}
</script>

<style>
.select-center {
    text-align: center;
}

.table th {
   text-align: center;
}

.table td {
    text-align: center; /* center checkbox horizontally */
    align-items: center;
    width: 16.666667%;
}

.table-content {
    padding-top: 40px;
    background-color: white;
    flex: 1 1 auto;
}

@media(max-width:992px){
    .table-content {
        padding-top: 0px !important;
    }
}
</style>
