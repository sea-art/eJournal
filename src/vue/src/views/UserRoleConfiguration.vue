<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-form-checkbox>Happy</b-form-checkbox>
            <b-table striped hover :items="items" :fields="fields"></b-table>
    </content-single-column>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import contentSingleColumn from '@/components/ContentSingleColumn.vue'

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
            fields: [
                { key: 'last_name'  },
                { key: 'first_name' },
                { key: 'age', label: 'Person age', variant: 'danger' }
            ],
            items: [
                { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
                { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
                { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
                { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
            ]
        }
    },
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb
    }
}
</script>
