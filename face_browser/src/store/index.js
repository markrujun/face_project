import Vue from 'vue'
import Vuex from 'vuex'

import user from './module/user'
import photo from './module/photo'
import alerter from './module/alerter'
import auditor from './module/auditor'
import checkItem from './module/checkItem'
import admin from './module/admin'

Vue.use(Vuex)

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      auditor,
      user,
      photo,
      alerter,
      checkItem,
      admin
    }
  })

  return Store
}
