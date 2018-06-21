<template>
    <b-card :class="$root.colors[uID % $root.colors.length]">
        <b-row>
            <b-col cols="4" sm="2">
                <img class="img-fluid portrait" src="@/assets/logo.png">
            </b-col>
            <b-col cols="8" order-sm="3" sm="4">
                 <b-form-select v-model="selectedRole" class="mb-3" :select-size="1">
                    <option :selected="role === 's'" value="s">Student</option>
                    <option :selected="role === 'ta'" value="ta">Teaching Assistant (TA)</option>
                    <option :selected="role === 't'" value="t">Teacher</option>
                 </b-form-select>
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
.portrait {
    max-height: 100px;
}
</style>
