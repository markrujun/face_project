import api from '../../api/api';
import router from '../../router';


const state = {
  token: '', // 登陆token
  islogin: true, // 是否登陆
  status: 0, // 当前状态 0 无记录
}


const getters = {

}



const mutations = {
  setToken(state, newToken) {
    state.token = newToken
    localStorage.setItem('adminToken', newToken)
  },
  setLogin(state) {
    state.islogin = true
  },
  setLogout(state) {
    state.islogin = false
    localStorage.removeItem('adminToken')
    router.push({path: '/check/login'})
  },
  setStatus(state, newStatus) {
    state.status = newStatus
  }
}

const actions = {
  getToken({ commit }, { username, password }) {
    api.getAdminToken(
      username, password,
      (info) => {
        if (info.data.code === 401) {
          commit('alerter/setMessage', "用户名密码错误！", { root: true })
          commit('setLogout')
        } else if (info.data.code === 201) {
          commit('setToken', info.data.token);
          router.push({path: '/check'})
          commit('setLogin')
        }
      }
    )
  },

}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
