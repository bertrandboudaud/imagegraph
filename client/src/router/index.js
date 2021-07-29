import Vue from 'vue';
import Router from 'vue-router';
import Main from '../components/Main.vue';
import Inputs from '../components/Inputs.vue';
import Outputs from '../components/Outputs.vue';

Vue.use(Router);
Vue.component('Inputs', Inputs);
Vue.component('Outputs', Outputs);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main,
    },
  ],
});
