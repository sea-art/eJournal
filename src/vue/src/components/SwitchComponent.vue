<template>
    <div>
        <label class="switch">
          <input type="checkbox" v-model="active">
          <span class="slider"></span>
        </label>
    </div>
</template>

<script>
export default {
    props: ['isActive'],
    computed: {
        active: {
            get: function () {
                return this.isActive
            },
            set: function (value) {
                this.$emit('parentActive', value)
            }
        }
    }
}
</script>

<style>
.switch {
    position: relative;
    display: inline-block;
    width: 48px;
    height: 26px;
}

.switch input {
    display:none;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
}

.slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
}

input:checked + .slider {
    background-color: var(--theme-blue);
}

input:focus + .slider {
    box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
    -webkit-transform: translateX(21px);
    -ms-transform: translateX(21px);
    transform: translateX(21px);
}
</style>
