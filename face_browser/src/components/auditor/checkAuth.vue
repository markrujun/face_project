<template>
    <div id="authpage" class="ma-10">

              <div style="padding-top:20vh;text-align:center;color:white">
                <h1>管理员登陆</h1>
              </div>
            <div style="margin:10vh 5vw">
              <v-form dark color="purple">
                <v-text-field dark prepend-icon="person" color="grey" name="login" label="用户名" type="text" v-model="tempUsername" ></v-text-field>
                <v-text-field dark id="password" prepend-icon="lock" color="grey" name="password" label="密码" type="password" v-model="tempPassword" @keyup.enter.native="login"></v-text-field>
              </v-form>
              <div style="color:white;text-align:center">
                <span></span>
              </div>
              <div style="margin:5vh;padding:5vw">
                <v-btn  block dark large round color="purple darken-4" @click="login">Login</v-btn>
              </div>
            </div>
        
      </div>
</template>

<script>
export default {
  name: 'loginForm',
  data(){
    return {
      tempUsername: '',
      tempPassword: '',
    }
  },
  props: {
    msg: String
  },
  watch: {
  },
  methods: {
    login () {
      if(this.tempUsername===''||this.tempPassword ===''){
        this.$store.commit('alerter/setMessage', "用户名密码不得为空。")
        return
      }
      this.$store.dispatch('auditor/getToken', {username:this.tempUsername, password:this.tempPassword})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #authpage{
    height: inherit;
    background: -webkit-linear-gradient( #4a148c , #fc00e7); /* Safari 5.1 - 6.0 */
    background: -o-linear-gradient(#4a148c, #fc00e7); /* Opera 11.1 - 12.0 */
    background: -moz-linear-gradient( #4a148c, #fc00e7); /* Firefox 3.6 - 15 */
    background: linear-gradient(#4a148c, #fc00e7); 
    height: 100vh;
    width: 100vw;
  }
  
</style>
