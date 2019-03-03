import api from '../../api/api'
const state = {
    islogin: true,
    token: '', // 登陆token
    // config
    configs: {
      host: '',
      photoLength: null,
      photoWidth: null,
      photoFormate: '',
      dir: '',
      confidence: null,
    },

    // userList
    userList: [],

    // check List
    checkList: [
      
      // {
      //  value: false,
      //  stuid: 161278019,
      //  name: "马如骏",
      //  systemPhoto: "https://api.zmrj.site/static/photo/gAAAAABb86g9NJTIYAMMlT7z5MXpG_UPqm1a2Nb3tACmQdmySl-OFLsDpdvXgekfV-UmChZkCUqS0OwuT8jRrRoeYuaW8L2YdQ.jpg",
      //  uploadPhoto: "https://api.zmrj.site/static/photo/gAAAAABb86g9NJTIYAMMlT7z5MXpG_UPqm1a2Nb3tACmQdmySl-OFLsDpdvXgekfV-UmChZkCUqS0OwuT8jRrRoeYuaW8L2YdQ.jpg",
      //  status: 2,
      //  confidence: 85,
      //  time: "12-02 21:36",
      //  auditor: "marujun",
      //  remark: null,
      // },
      ],
      adminList: [
        {
          adminname: '',
          premission: '',
        }
      ],
      
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
  },
  setConfig(state, data) {
    state.configs.host =  data['app_HOST']
    state.configs.photoLength = data['app_PHOTO_LENGTH']
    state.configs.photoWidth = data['app_PHOTO_WIDTH']
    state.configs.photoFormat = data['app_PHOTO_FORMAT'].slice(1)
    state.configs.dir = data['app_PHOTO_DIR']
    state.configs.confidence = data['app_CONFIDENCE']
  },
  setUserList(state, data) {
    state.userList = data
  },
  setCheckList(state, data) {
    state.checkList = data.checkList
  },
  setAdminList(state, data) {
    state.adminList = data.adminList
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
          commit('alerter/setMessage', "登陆成功", { root: true })
          commit('setToken', info.data.token);
          commit('setLogin')
        }
      }
    )
  },
  getConfig({commit}) {
    return new Promise((resolve) => {
      api.getConfig(
        (info) => {
          if(info.data.code == 201){
            commit('setConfig', info.data);
          } else if(info.data.code == 403) {
            commit('alerter/setMessage', "您的权限不足，无法获取数据！", { root: true })
          } else if(info.data.code == 401) {
            commit('setLogout');
            commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
          } else {
            commit('alerter/setMessage', "未知错误！", { root: true })
          }
          resolve({
            host : info.data['app_HOST'],
            photoLength : info.data['app_PHOTO_LENGTH'],
            photoWidth : info.data['app_PHOTO_WIDTH'],
            photoFormat : info.data['app_PHOTO_FORMAT'].slice(1),
            dir : info.data['app_PHOTO_DIR'],
            confidence : info.data['app_CONFIDENCE']
          })
        }
      )
    })
  },
  saveConfig({commit, dispatch},{configData}) {
    api.saveConfig(
      configData.host, configData.photoLength, configData.photoWidth, configData.photoFormat, configData.dir, configData.confidence,
        (info) => {
          if(info.data.code == 201){
            commit('alerter/setMessage', "修改成功！", { root: true })
            dispatch('getConfig')
          } else if(info.data.code == 403) {
            commit('alerter/setMessage', "您的权限不足，无法获取数据！", { root: true })
          } else if(info.data.code == 401) {
            commit('setLogout');
            commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
          } else {
            commit('alerter/setMessage', "未知错误！", { root: true })
          }
        }
    )
  },
  getUserList({commit, dispatch}) {
    api.getUserList(
      (info) => {
        if(info.data.code === 200) {
          commit('setUserList', info.data.userList)
        } else if(info.data.code == 401) {
          commit('setLogout', {task: dispatch('getUserList')});
          commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
        }
      }
    )
  },
  getCheckList({commit}) {
    api.getCheckList(
      (info) => {
        if(info.data.code == 201){
          commit('setCheckList', info.data);
        } else if(info.data.code == 403) {
          commit('alerter/setMessage', "您的权限不足，无法获取数据！", { root: true })
        } else if(info.data.code == 401) {
          commit('setLogout');
          commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
        } else {
          commit('alerter/setMessage', "未知错误！", { root: true })
        }
      }
    )
  },
  editCheckItem({commit,dispatch}, {username,status, remark}) {
    api.editCheckItem(username,status, remark,
      (info) => {
        if(info.data.code == 201){
          commit('alerter/setMessage', "修改成功！", { root: true })
          dispatch('getCheckList')
        } else if(info.data.code == 403) {
          commit('alerter/setMessage', "您的权限不足，无法获取数据！", { root: true })
        } else if(info.data.code == 401) {
          commit('setLogout');
          commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
        } else {
          commit('alerter/setMessage', "未知错误！", { root: true })
        }
      }
    )
  },
  addSingleUser({commit,dispatch}, {username, password, photo}) {
    api.addSingleUser(username, password, photo, 
      (info) => {
        if(info.data.code == 201){
          commit('alerter/setMessage', "添加成功！", { root: true })
          dispatch('getUserList')
        } else if(info.data.code == 403) {
          commit('alerter/setMessage', "您的权限不足，无法获取数据！", { root: true })
        } else if(info.data.code == 401) {
          commit('setLogout');
          commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
        } else if(info.data.code == 409) {
          commit('alerter/setMessage', "用户名已存在！", { root: true })
        } else {
          commit('alerter/setMessage', "未知错误！", { root: true })
        }
      }
      )
  },
  deleteUser({commit,dispatch}, {username}) {
    api.deleteUser(username, (info)=>{
      if(info.data.code == 200){
        commit('alerter/setMessage', "删除成功！", { root: true })
        dispatch('getUserList')
      } else if(info.data.code == 403) {
        commit('alerter/setMessage', "您的权限不足，无法删除数据！", { root: true })
      } else if(info.data.code == 401) {
        commit('setLogout');
        commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
      } else if(info.data.code == 400) {
        commit('alerter/setMessage', "不存在该用户！", { root: true })
      } else {
        commit('alerter/setMessage', "未知错误！", { root: true })
      }
    })
  },
  addUsers({commit, dispatch}, {data, zipFile}) {
    return new Promise((resolve) => {
      api.addUsers(data, zipFile, 
        (info)=> {
          if(info.data.code == 201){
            commit('alerter/setMessage', "处理成功！", { root: true })
            dispatch('getUserList')
          } else if(info.data.code == 403) {
            commit('alerter/setMessage', "您的权限不足，无法删除数据！", { root: true })
          } else if(info.data.code == 401) {
            commit('setLogout');
            commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
          } else if(info.data.code == 400) {
            commit('alerter/setMessage', "不存在该用户！", { root: true })
          } else {
            commit('alerter/setMessage', "未知错误！", { root: true })
          }
          resolve({
            successList: info.data.successList,
            failedList: info.data.failedList
          })
        }
      )
    })
  },
  getAdminList({commit}) {
    api.getadminList(
      (info) => {
        if(info.data.code == 200){
          commit('setAdminList', info.data);
        } else if(info.data.code == 403) {
          commit('alerter/setMessage', "您的权限不足，无法获取数据！", { root: true })
        } else if(info.data.code == 401) {
          commit('setLogout');
          commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
        } else {
          commit('alerter/setMessage', "未知错误！", { root: true })
        }
      }
    )
  },
  addAdmin({commit, dispatch}, {adminname, password, permission}) {
    api.addAdmin(adminname, password, permission,
      (info) => {
        if(info.data.code == 201){
          commit('alerter/setMessage', "添加成功！", { root: true })
          dispatch('getAdminList')
        } else if(info.data.code == 403) {
          commit('alerter/setMessage', "您的权限不足，无法获取数据！", { root: true })
        } else if(info.data.code == 401) {
          commit('setLogout');
          commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
        } else if(info.data.code == 409) {
          commit('alerter/setMessage', "管理员已存在！", { root: true })
        } else {
          commit('alerter/setMessage', "未知错误！", { root: true })
        }
      }
      ) 
  },
  deleteAdmin({commit, dispatch}, {adminname}) {
    api.deleteAdmin(adminname, 
      (info)=> {
        if(info.data.code == 200){
          commit('alerter/setMessage', "处理成功！", { root: true })
          dispatch('getAdminList')
        } else if(info.data.code == 403) {
          commit('alerter/setMessage', "您的权限不足，无法删除数据！", { root: true })
        } else if(info.data.code == 401) {
          commit('setLogout');
          commit('alerter/setMessage', "登陆失效，请重新登录！", { root: true })
        } else if(info.data.code == 400) {
          commit('alerter/setMessage', "不存在该管理员！", { root: true })
        } else {
          commit('alerter/setMessage', "未知错误！", { root: true })
        }
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
