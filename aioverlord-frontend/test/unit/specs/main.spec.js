import Vue from 'vue';
import main from '@/components/main';

describe('main.vue', () => {
  it('should render correct contents', () => {
    const Constructor = Vue.extend(main);
    const vm = new Constructor().$mount();
    expect(vm.$el.querySelector('h1').textContent)
      .to.equal('AI Overlord');
  });
});
