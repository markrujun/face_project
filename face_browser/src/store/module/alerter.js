
const state = {
    message: '',
    show: true
}


const getters = {

}



const mutations = {
  setMessage(state,message){
    state.message = message
    state.show = !state.show
  },
  show(state) {
    state.show = !state.show
  }
}

const actions = {
  
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
