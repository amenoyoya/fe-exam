// Vue
import Vue from 'vue';
import 'babel-polyfill'; // IE11 polyfill

// Buefy
import Buefy from 'buefy';
import 'buefy/dist/buefy.css';
Vue.use(Buefy);

// components
import Home from './components/Home';

new Vue({
  render: h => h(Home)
}).$mount('#app');
