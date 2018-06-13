import Vue from 'vue'
import Home from '@/views/Home'
import router from '@/router'

describe('Home.vue', () => {
    it('should render correct contents', () => {
        const Constructor = Vue.extend(Home)
        const vm = new Constructor({router}).$mount()
        expect(vm.$el.querySelector('h1').textContent)
            .to.equal('\n        Courses\n    ')
    })
})
