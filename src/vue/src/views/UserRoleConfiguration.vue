<template>
    <b-row no-gutters>
        <b-col cols="12" lg="6" offset-lg="3" class="table-content">
            <bread-crumb>&nbsp;</bread-crumb>


            <b-button class="multi-form float-right add-button ml-2"> Update </b-button>
            <b-button class="multi-form float-right delete-button"> Reset </b-button>

            <table class="table table-bordered table-hover">
                <thead >
                    <tr v-if="windowWidth > 750">
                        <th/>
                        <th v-for="role in roles" :key="'th-' + role">{{ role }}</th>
                        <th><icon name="plus-square" @click.native="modalShow = !modalShow" class="add-icon" scale="1.75"></icon></th>
                    </tr>
                    <tr v-else>
                        <th/>
                        <b-form-select
                            class="select-center mb-3"
                            v-model="selectedRole"
                            :options="selectRoles"/>
                        <th><icon name="plus-square" @click.native="modalShow = !modalShow" class="add-icon" scale="1.75"></icon></th>
                    </tr>
                </thead>
                <tbody v-if="windowWidth > 750">
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
                <tbody v-else>
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

            <b-modal
                @shown="focusRoleNameInput"
                title="Role creation"
                size="lg"
                v-model="modalShow"
                hide-footer>
                <b-form-input
                    @keyup.enter.native="addRole"
                    v-model="newRole"
                    class="multi-form"
                    ref="roleNameInput"
                    required placeholder="Role name"/>
                <b-button @click="addRole" class="add-button">Create role</b-button>
                <b-button @click="modalShow = false" class="delete-button">Cancel</b-button>
            </b-modal>

        </b-col>
    </b-row>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import customCheckbox from '@/components/CustomCheckbox.vue'
import icon from 'vue-awesome/components/Icon'

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
            defaultRoles: [],
            defaultPermissions: [],
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
            modalShow: false,
            newRole: '',
            windowWidth: 550
        }
    },
    methods: {
        getWindowWidth (event) {
            this.windowWidth = document.documentElement.clientWidth
        },
        updateRole (list) {
            console.log(list)
        },
        addRole () {
            this.modalShow = false
            this.roles.push(this.newRole)
            this.newRole = ''
        },
        focusRoleNameInput () {
            this.$refs.roleNameInput.focus()
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
        'custom-checkbox': customCheckbox,
        icon
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
