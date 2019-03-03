<template>
  <v-layout row justify-center>
    <v-dialog v-model="openLogin" persistent max-width="500">
      <v-card>
        <v-card-title class="headline">请先登录</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
            <v-container>
                <v-text-field
                    label="用户名"
                    v-model="tempUsername"
                ></v-text-field>
                <v-text-field
                    label="密码"
                    type="password"
                    v-model="tempPassword"
                ></v-text-field>
            </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary darken-1"  @click="login">登陆</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>
<script>
import { mapState } from 'vuex'
  export default {

    data () {
      return {
        tempUsername:'',
        tempPassword:'',
      }
    },
    computed:{
        openLogin:{
            get: function () {
                return !(this.$store.state.admin.islogin);
            },
        }
    },
    methods: {
        login () {
        if(this.tempUsername===''||this.tempPassword ===''){
            this.$store.commit('alerter/setMessage', "用户名密码不得为空。")
            return
        }
        this.$store.dispatch("admin/getToken", {username: this.tempUsername, password: this.tempPassword});
        },
    }

  }
</script>