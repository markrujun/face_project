import api from '../../api/api'

const state = {
  photoUrl: '',
  photoBlob: null,
  server_status: 0, // 0表示从未上传，1表示上传后未审核，2表示审核未通过
  browser_status: 0, // 0表示未添加图片， 1表示添加后未上传
  isUploading: false,
  uploadRes: ''
}


const getters = {
  message(state) {
    if(state.server_status===0) {
      if( state.browser_status === 0) {
        return "请从相册中选择合适证件照上传"
      } else {
        return "照片尚未上传审核， 请确认后上传审核"
      }
    } else if( state.server_status===1 ) {
      return "您的照片正在审核阶段"
    } else if (state.server_status===2) {
      return "您的照片已通过人脸识别检验， 正在等待管理员审核"
    }else if( state.server_status===3) {
      return "您的照片审核未通过"
    } else if( state.server_status===4) {
      return "您的照片审核成功"
    } else {
      return "未知状态"
    }
  }
}



const mutations = {
  setPhoto(state,photoUrl){
    state.photoUrl = photoUrl
  },
  setPhotoBlob(state,photoBlob){
    state.photoBlob = photoBlob
  },
  setBrowserStatus(state) {
    if(state.browser_status===0) {
      state.browser_status =1
    }
  },
  setServerStatus(state, status){
    state.server_status = status
  },
  setUploading(state, val) {
    state.isUploading = val
  },
  setUploadRes( state, val) {
    state.uploadRes = val
  } 
}

const actions = {
  getPhoto({commit}) {
    if(!localStorage.getItem('token')){
      commit('user/setLogout', {},{root: true})
      return
    }
    api.getPhoto(
      (info) => {
        if(info.data.code === 401) {
          commit('user/setLogout', {},{root: true})
          commit('alerter/setMessage', "登陆已失效。",{root: true})
        } else {
          commit('setPhoto',info.data.photoUrl)
          commit('setServerStatus', info.data.status)
        }
      }
    )
  },
  uploadPhoto({state, commit, dispatch}) {
    const img = state.photoBlob
    commit('setUploading', true)
    commit('setUploadRes', "照片正在上传审核中，请稍等>>>>>")
    
    api.uploadPhoto(img,
      (info) => {
        if( info.data.code === 200 && info.data.status===1) {
          commit('setServerStatus', info.data.status)
          commit('setUploadRes', `对不起，您的照片无法识别为本人，置信度${info.data.confidence}`)
          dispatch('getPhoto')
          commit('setUploading', false)
        } else if(info.data.code === 200 && info.data.status===2){
          commit('setServerStatus', info.data.status)
          commit('setUploadRes', `您的照片已成功识别为本人，置信度${info.data.confidence}`)
          commit('setUploading', false)
        } else if(info.data.code === 500) {
          commit('setUploadRes', "该用户不存在")
          commit('user/setLogout', {}, {root: true})
          commit('setUploading', false)
        } else {
          commit('alerter/setMessage', "未知错误。",{root: true})
        }
      },
      () => {
          commit('alerter/setMessage', "网络错误。",{root: true})
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
