<template>
  <v-layout id="checkPage" fill-height column overflow-hidden>
    <div id="header">
      <!-- 5vh -->
      <v-btn fab small top right @click="logout">
        <v-icon>logout</v-icon>
      </v-btn>
    </div>
    <v-layout v-if="!free" column fill-height overflow-hidden>
      <!-- picture -->
      <v-layout align-center justify-space-around row fill-height overflow-hidden>
        <v-responsive style="margin:50px 20px 0 20px;" :max-width="200"  :aspect-ratio="16/9">
          <v-img   class="animated" :class="{bounceInRight:!change, bounceOutLeft: change}" :src="originPhotoUrl">

          </v-img>
        </v-responsive>
        <v-responsive  style="margin:50px 20px 0 20px;" :max-width="200"  :aspect-ratio="9/16">
          <v-img  class="animated" :class="{bounceInRight:!change, bounceOutLeft: change}"  :src="eventPhotoUrl">

          </v-img>
          <!-- <v-img v-else class="animated" :class="{bounceInRight:change, 'delay-2s':change}" :src="eventPhotoUrl">

          </v-img> -->
        </v-responsive>
      </v-layout>
      <v-layout align-center justify-space-around row fill-height overflow-hidden>
        <v-btn fab dark large color="error"  @click="dialog=true">
          <v-icon dark>clear</v-icon>
        </v-btn>
        <v-btn fab dark large color="success" @click="pass">
          <v-icon dark>done</v-icon>
        </v-btn>
      </v-layout>
    </v-layout>
    <v-layout id="free" v-else align-center justify-center  column fill-height overflow-hidden>
      <v-layout align-center justify-space-around row fill-height overflow-hidden>
        <h2>辛苦啦，暂无需要审核的照片</h2>
      </v-layout>
      <v-layout align-center justify-space-around row fill-height overflow-hidden>

      </v-layout>
    </v-layout>
    <v-dialog v-model="dialog" persistent >
      <v-card>
        <v-card-title>
          <span class="headline">请输入理由</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="reason" label="不通过理由" required></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="dialog = false">取消</v-btn>
          <v-btn color="blue darken-1" flat @click="unpass">提交</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>
<script>
import {mapState} from 'vuex'
export default {
    data() {
        return {
          dialog: false,
          reason: '',
        }
    },
    methods: {
        logout() {
          this.$store.commit("auditor/setLogout");
        },
        pass() {
          this.$store.dispatch("checkItem/pass", {mark: '', pass: true})
        },
        unpass() {
          this.$store.dispatch("checkItem/unpass", {mark: this.reason, pass: false})
          this.dialog = false
        }
    },
    created() {
      if(!localStorage.getItem("adminToken")) {
      this.$store.commit('alerter/setMessage', "请先登录。")
      this.$store.commit("auditor/setLogout");
      return;
    }
      this.$store.dispatch("checkItem/getCheckItem");
    },
    computed: {
        ...mapState('checkItem', {
            eventPhotoUrl: 'eventPhotoUrl',
            originPhotoUrl: 'originPhotoUrl',
            change: 'change',
            free: 'free'
        })
    }
}
</script>
<style>
#free{
  background:url('../../assets/IMAGE.jpg');
  background-size: 100% 100%;
}
#checkPage{
  width: 100vw;
  height: 100vh;
}
#header {
  height: 5vh;
  width: 100vw;
  background-color: #4a148c;
  background: -webkit-linear-gradient(
    left,
    #4a148c,
    #6201d8
  ); /* Safari 5.1 - 6.0 */
  background: -o-linear-gradient(
    right,
    #4a148c,
    #6201d8
  ); /* Opera 11.1 - 12.0 */
  background: -moz-linear-gradient(
    right,
    #4a148c,
    #6201d8
  ); /* Firefox 3.6 - 15 */
  background: linear-gradient(to right, #4a148c, #6201d8); /* 标准的语法 */
}
</style>


