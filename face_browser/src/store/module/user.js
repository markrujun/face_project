import authentication from '../../api/api'
import router from '../../router';

const state = {
  token: '', // 登陆token
  islogin: true, // 是否登陆
  status: 0, // 当前状态 0 无记录
  photoUrl: ''
}


const getters = {

}



const mutations = {
  setToken(state, newToken) {
    state.token = newToken
    localStorage.setItem('token', newToken)
  },
  setLogin(state) {
    state.islogin = true
  },
  setLogout(state) {
    state.islogin = false
    localStorage.removeItem('token')
    router.push({path: '/user/login'})
  },
  setStatus(state, newStatus) {
    state.status = newStatus
  },
  setPhoto(photoUrl) {
    state.photoUrl = photoUrl
  }
}

const actions = {
  getToken({ commit }, { username, password }) {
    authentication.getToken(
      username, password,
      (info) => {
        if (info.data.code === 401) {
          commit('alerter/setMessage', "用户名密码错误！", { root: true })
          commit('setLogout')
        } else if (info.data.code === 201) {
          commit('setToken', info.data.token);
          router.push({path: '/user'})
          commit('setLogin')
        }
      }
    )
  },
  register({ commit }, { username, password, phone }) {
    authentication.register(
      username, password, phone,
      () => {
        commit('alerter/setMessage', "注册成功。", { root: true })
        return 'success'
      }
    )
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
