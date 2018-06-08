import Vue from 'vue'
import Home from '@/components/Home'
import router from '@/router'

describe('Home.vue', () => {
    it('should render correct contents', () => {
        const Constructor = Vue.extend(Home)
        const vm = new Constructor({router}).$mount()
        expect(vm.$el.querySelector('.home h1').textContent)
            .to.equal('Courses')
    })
    it('sets the correct default data', () => {
        expect(typeof Home.data).equal('function')
        const defaultData = Home.data()
        expect(defaultData.msg).equal('Courses')
    })
})
