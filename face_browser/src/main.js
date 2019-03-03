import Vue from 'vue'
import './plugins/vuetify'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
// import './plugins/vuetify'
// import Vuetify from 'vuetify/lib'
// import 'vuetify/src/stylus/app.styl'
// import 'animate.css'
import App from './App.vue'
import router from './router'
import store from './store/index'
// import './registerServiceWorker'

// Vue.use(Vuetify)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
