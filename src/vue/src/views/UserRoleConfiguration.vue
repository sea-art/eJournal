<template>
    <content-single-table-column>
        <bread-crumb>&nbsp;</bread-crumb>

        <b-button @click="update()" class="multi-form float-right add-button ml-2"> Save </b-button>
        <b-button @click="reset()" class="multi-form float-right delete-button"> Reset </b-button>

        <div class="table-responsive">
            <table class="table table-bordered table-hover">
                <thead>
                    <tr>
                        <th/>
                        <th v-for="role in roles" :key="'th-' + role">
                            {{ role }}
                            <icon
                                v-if="!undeleteableRoles.includes(role)"
                                name="trash" @click.native="deleteRole(role)"
                                class="trash-icon"
                                scale="1.25"/>
                        </th>
                        <th><icon name="plus-square" @click.native="modalShow = !modalShow" class="add-icon" scale="1.75"/></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="permission in permissions" :key="permission">
                        <td class="permission-column">{{ formatPermissionString(permission) }}</td>
                        <td v-for="role in roles" :key="role + '-' + permission">
                            <custom-checkbox
                            @checkbox-toggle="updateRole"
                            :role="role"
                            :permission="permission"
                            :receivedState="setState(role, permission)"/>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

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
    </content-single-table-column>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import contentSingleTableColumn from '@/components/ContentSingleTableColumn.vue'
import customCheckbox from '@/components/CustomCheckbox.vue'
import icon from 'vue-awesome/components/Icon'
import permissions from '@/api/permissions.js'

export default {
    name: 'UserRoleConfiguration',
    props: {
        cID: {
            required: true
        }
    },
    data () {
        return {
            roles: [],
            permissions: [],
            backupPermissions: [],
            roleConfig: [],
            originalRoleConfig: [],
            defaultRoles: [],
            selectRoles: [
                {value: null, text: 'Please select a role'},
                {value: 'Student', text: 'Student'},
                {value: 'TA', text: 'TA'},
                {}
            ],
            undeleteableRoles: ['Student', 'TA', 'Teacher'],
            selectedRole: null,
            modalShow: false,
            newRole: '',
            windowWidth: 550
        }
    },
    methods: {
        updateRole (list) {
            var role = list[0]
            var permission = list[1]
            var state = list[2]

            var i = this.roleConfig.findIndex(p => p.name === role)

            this.roleConfig[i].permissions[permission] = (state ? 1 : 0)
        },
        callocRoleObject (role) {
            /* Initialises a role object with the given name, the pages cID
             * and permissions object with all  corresponding permissions set to false. */
            var newPermissions = {}

            for (var i = 0; i < this.permissions.length; i++) {
                newPermissions[this.permissions[i]] = 0
            }

            return { name: role, cID: this.cID, permissions: newPermissions }
        },
        deepCopyRoles (roles) {
            var deepCopy = []

            for (var i = 0; i < roles.length; i++) {
                var permissions = {}

                for (var j = 0; j < this.permissions.length; j++) {
                    permissions[this.permissions[j]] = roles[i].permissions[this.permissions[j]]
                }

                deepCopy.push({ name: roles[i].name, cID: this.cID, permissions: permissions })
            }

            return deepCopy
        },
        addRole () {
            /* Adds a new role, clearing the input buffer and updating the
             * roles list and roleconfiguration objects. */
            this.roleConfig.push(this.callocRoleObject(this.newRole))
            this.roles.push(this.newRole)

            this.modalShow = false
            this.newRole = ''
        },
        focusRoleNameInput () {
            /* Ensures the modal name field is focused upon the modal opening. */
            this.$refs.roleNameInput.focus()
        },
        setState (role, permission) {
            var correctRole = (this.roleConfig.filter(arg => { return arg.name === role }))[0]
            return correctRole.permissions[permission] === 1
        },
        reset () {
            /* Resets the configuration to the defaults by deep copies.
             * Forces reupdate of custom checkbox components,
             * by temporarily clearing the roles and permissions lists.
             * This could be prevented by creating a custom data model which
             * could interact with v-model.
             * However scaling should not be a problem here (time choice to keep
             * working with the databse given format.)  */
            if (confirm('This will undo all unsaved work\n Are you sure you want to continue?')) {
                this.roleConfig = this.deepCopyRoles(this.originalRoleConfig)

                this.roles = []
                this.backupPermissions = Array.from(this.permissions)
                this.permissions = []
                this.$nextTick(() => {
                    this.roles = Array.from(this.defaultRoles)
                    this.permissions = this.backupPermissions
                })
            }
        },
        update () {
            permissions.update_course_roles(this.cID, this.roleConfig)
                .then(response => {
                    this.originalRoleConfig = this.deepCopyRoles(this.roleConfig)
                    this.defaultRoles = Array.from(this.roles)
                    this.$toasted.success('Update succesfull!')
                })
                .catch(_ => this.$toasted.error('Something went wrong when updating the permissions'))
        },
        formatPermissionString (str) {
            /* Converts underscores to spaces and capatilises the first letter. */
            var temp = str.split('_').join(' ')
            return temp[0].toUpperCase() + temp.slice(1)
        },
        deleteRole (role) {
            if (confirm('Are you sure you want to delete role: ' + role + 'entirely?')) {
                if (this.defaultRoles.includes(role)) {
                    /* handle server update. */
                    permissions.delete_course_role(this.cID, role)
                        .then(response => {
                            this.deleteRoleLocalConfig(role)
                            this.deleteRoleServerLoadedConfig(role)
                            this.$toasted.success('Role deleted succesfully!')
                        })
                        .catch(_ => this.$toasted.error('Something went wrong when deleting role: ' + role))
                } else {
                    this.deleteRoleLocalConfig(role)
                }
            }
        },
        deleteRoleLocalConfig (role) {
            var i = this.roleConfig.findIndex(p => p.name === role)
            this.roleConfig.splice(i, 1)
            i = this.roles.findIndex(p => p === role)
            this.roles.splice(i, 1)
        },
        deleteRoleServerLoadedConfig (role) {
            var i = this.originalRoleConfig.findIndex(p => p.name === role)
            this.originalRoleConfig.splice(i, 1)
            i = this.defaultRoles.findIndex(p => p === role)
            this.defaultRoles.splice(i, 1)
        }
    },
    created () {
        /* Initialises roles, permissions and role config as well as their defaults.
         * Roles and Permissions objects need to exist as deepcopy depends on then. */
        permissions.get_course_roles(this.cID)
            .then(response => {
                this.roleConfig = response

                response.forEach(role => {
                    this.defaultRoles.push(role.name)
                })
                this.permissions = Object.keys(response[0].permissions)
                this.roles = Array.from(this.defaultRoles)

                this.originalRoleConfig = this.deepCopyRoles(response)
            })
            .catch(_ => this.$toasted.error('Error while loading course roles'))
    },
    components: {
        'content-single-table-column': contentSingleTableColumn,
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

.permission-column {
    text-align: left !important;
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
