<template>
    <div id="authpage" class="ma-10">
        <!-- <v-window v-model="onboarding">
          <v-window-item> -->
              <div style="padding-top:20vh;text-align:center;color:white">
                <h1>登陆</h1>
              </div>
            <div style="margin:10vh 5vw">
              <v-form dark color="purple">
                <v-text-field dark prepend-icon="person" color="grey" name="login" label="用户名" type="text" v-model="tempUsername" ></v-text-field>
                <v-text-field dark id="password" prepend-icon="lock" color="grey" name="password" label="密码" type="password" v-model="tempPassword" @keyup.enter.native="login"></v-text-field>
              </v-form>
              <div style="color:white;text-align:center">
                <!-- <span v-if="onboarding!==index" @click="onboarding = index" v-for="(i, index) in tabs" :key="index" style="margin:0 10px;">{{i}} </span> -->
                <span v-for="(i, index) in tabs" :key="index" style="margin:0 10px;">{{i}} </span>
              </div>
              <div style="margin:5vh;padding:5vw">
                <v-btn  block dark large round color="purple darken-4" @click="login">Login</v-btn>
              </div>
            </div>
          <!-- </v-window-item>
          <v-window-item>
            <div style="padding-top:20vh;text-align:center;color:white">
              <h1>注册</h1>
            </div>
            <div style="margin:10vh 5vw">
            <v-form dark color="purple">
              <v-text-field dark prepend-icon="person" color="grey" name="login" label="请输入用户名" type="text" v-model="tempUsername1"></v-text-field>
              <v-text-field dark id="password1" prepend-icon="lock" color="grey" name="password" label="请输入密码" type="password" v-model="tempPassword1"></v-text-field>
              <v-text-field dark id="password2" prepend-icon="lock" color="grey" name="password" label="请确认密码" type="password" v-model="tempPassword2"></v-text-field>
              <v-text-field dark id="phone" prepend-icon="phone" color="grey" name="phone" label="请输入手机号"  v-model="tempPhone" @keyup.enter.native="register"></v-text-field>
            </v-form>
            <div style="color:white;text-align:center">
              <span v-if="onboarding!==index" @click="onboarding = index" v-for="(i, index) in tabs" :key="index" style="margin:0 10px;">{{i}} </span>
            </div>
            <div style="margin:5vh;padding:5vw">
              <v-btn  block dark large round color="purple darken-4" @click="register">register</v-btn>
            </div>
          </div>
          </v-window-item>
        </v-window> -->
        
      </div>
</template>

<script>
export default {
  name: 'loginForm',
  data(){
    return {
      tempUsername: '',
      tempPassword: '',
      tempUsername1: '',
      tempPassword1: '',
      tempPassword2: '',
      tempPhone: '',
      onboarding: 0,
      // tabs: ["已有账号，立即登陆","没有账号？立即注册"]
      tabs: [" ",]
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
      this.$store.dispatch('user/getToken', {username:this.tempUsername, password:this.tempPassword})
    },
    // register() {
    //   if(this.tempUsername1 === ''||this.tempPassword1 === ''|| this.tempPhone === ''|| this.tempPassword2 === '') {
    //     this.$store.commit('alerter/setMessage', "字段不得为空。")
    //     return
    //   }
    //   if(this.tempPassword1 !== this.tempPassword2){
    //     this.$store.commit('alerter/setMessage', "两次输入密码不一致。")
    //     return
    //   }
    //   this.$store.dispatch('user/register', {username:this.tempUsername1, password:this.tempPassword1, phone: this.tempPhone})
    // }
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
