import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/user',
      component: () => import(/* webpackChunkName: 'userViews' */'./views/user.vue'),
      children: [
        { path: '/', component: () => import(/* webpackChunkName: 'userIndex' */'./components/user/index.vue'), name: 'index'},
        { path: 'login', component: () => import(/* webpackChunkName: 'userAuth' */'./components/user/auth.vue'), name: 'auth'}
      ]
    },
    {
      path: '/check',
      component: () => import(/* webpackChunkName: 'auditorViews' */'./views/auditor.vue'),
      children: [
        { path: '/', component: () => import(/* webpackChunkName: 'checkIndex' */'./components/auditor/checkIndex.vue'), name: 'index'},
        { path: 'login', component: () => import(/* webpackChunkName: 'checkAuth' */'./components/auditor/checkAuth.vue'), name: 'auth'}
      ]
    },
    {
      path: '/admin',
      component: () => import(/* webpackChunkName: 'adminViews' */'./views/admin.vue'),
      children: [
        { path: '/', redirect: 'checkList'},
        { path: 'checkList', component: () => import(/* webpackChunkName: 'checckList' */'./components/admin/check/checkList.vue'), name: 'checkList' },
        { path: 'photoList', component: () => import(/* webpackChunkName: 'photoList' */'./components/admin/check/photoList.vue'), name: 'photoList' },
        { path: 'adminList', component: () => import(/* webpackChunkName: 'adminList' */'./components/admin/user/adminList.vue'), name: 'adminList' },
        { path: 'addUsers', component: () => import(/* webpackChunkName: 'addUsers' */'./components/admin/user/addUsers.vue'), name: 'addUsers' },
        { path: 'userList', component: () => import(/* webpackChunkName: 'userList' */'./components/admin/user/userList.vue'), name: 'userList' },
        { path: 'systemConfig', component: () => import(/* webpackChunkName: 'sysConfig' */'./components/admin/config/systemConfig.vue'), name: 'systemConfig' },
      ]
    }
  ]
})
  