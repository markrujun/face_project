import api from '../../api/api'

const state = {
  id: 0,
  eventPhotoUrl: '',
  originPhotoUrl: '',
  change: false,
  free: true
}


const getters = {
}



const mutations = {
    setPhoto(state, {eventPhotoUrl,originPhotoUrl}) {
        state.eventPhotoUrl = eventPhotoUrl
        state.originPhotoUrl = originPhotoUrl
    },
    setId(state, id) {
        state.id = id
    },
    setChange(state, {change}){
        state.change = change
    },
    setFree(state,free){
        console.log(free);
        
        state.free = free
    }
}

const actions = {
    getCheckItem({commit}) {
        api.getCheckItem(
            (info) => {
                if( info.data.code === 200 ) {
                    commit('setPhoto', {"eventPhotoUrl":info.data.eventPhotoUrl, "originPhotoUrl": info.data.originPhotoUrl} )
                    commit('setFree',false)
                    commit('setChange',false)
                    commit('setId', info.data.id)
                } else if (info.data.code === 204) {
                    commit('setFree',true)
                } else if (info.data.code === 401) {
                    commit('auditor/setLogout', {}, {root: true})
                    commit('alerter/setMessage', '登陆失效', {root: true})
                } else {
                    commit('alerter/setMessage', '数据库读取失败', {root: true})
                }
            },
            () => {
                commit('alerter/setMessage', '网络错误', {root: true})
            }
        )
      },
    pass({state,commit,dispatch}, {mark}) {
        // commit('setChange', true)
        api.postCheckItem(
            state.id, true, mark,
            (info) => {
                console.log(info);
                if( info.data.code === 201){
                    commit('alerter/setMessage', '审核成功', {root: true})
                    dispatch('getCheckItem')
                }
            },
            (error) => {
                console.log(error);
            }
        )
    },
    unpass({state}, {mark}) {
        api.postCheckItem(
            state.id, false, mark,
            (info) => {
                if( info.data.code === 201){
                    commit('alerter/setMessage', '审核成功', {root: true})
                    dispatch('getCheckItem')
                }
            },
            (error) => {
                console.log(error);
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
