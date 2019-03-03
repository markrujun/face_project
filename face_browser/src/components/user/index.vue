<template>
  <div id="checkPage">
    <v-layout full-height align-center justify-center column>
      <div id="header">
        <!-- 5vh -->
        <v-btn fab small top right @click="logout">
          <v-icon>logout</v-icon>
        </v-btn>
      </div>

      <div id="photoArea">
        <!-- 30vh -->
        <!-- <v-avatar
                        :tile="true"
                        :size="110"
                        color="grey lighten-4"
                    > -->
        <v-img :src="photoUrl" height="175" contain style="align-self:center"></v-img> <!-- 固定 -->
        <!-- </v-avatar> -->
      </div>
      <div style="margin:2vh 7vw;height:5vh">
        <!-- 9vh -->
        <h3 class="text-md-center">{{message}}</h3>
      </div>
      <v-container style="height:15vh" grid-list-md text-xs-center>
        <!-- 15vh -->
        <v-layout row wrap>
          <v-flex xs6>
            <v-btn fab large color="transparent">
              <label style="height:72px;width:72px;display:block;border-radius: 50%;" for="imageInput">
                <v-icon dark>photo_library</v-icon>
              </label>
            </v-btn>
            <input @change="upload" type="file" accept="image/*" id="imageInput" style="display:none" name="imageInput">
          </v-flex>
          <v-flex xs6>
            <v-btn @click="crop" fab large color="transparent">
              <v-icon dark>crop</v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
        <v-layout row >
          <v-flex xs6>
            相册
          </v-flex>
          <v-flex xs6>
            裁剪
          </v-flex>
        </v-layout>
      </v-container>
      <div style="width:90vw;height:20vh;display:flex;">
        <v-btn style="align-self:center" :loading="isUploading" :disabled="isUploading" @click="submit" block :dark="!isUploading" large round color="purple darken-4">上传审核<v-icon right dark>cloud_upload</v-icon>
        </v-btn>
      </div>
      <div class="shadow justify-center" v-if="shadowOn">
        <div class="loading">
          <v-progress-circular indeterminate color="purple" :size="60"></v-progress-circular>
          <p style="margin:5px 0;font-size:17px;">读取中...</p>
        </div>
      </div>
    </v-layout>
    <v-dialog v-model="cropOpen" lazy fullscreen hide-overlay transition="dialog-bottom-transition">
      <cropContent @finish="finishCrop" :cropImage="image" @close="cropOpen=false" :quality="quality" />
    </v-dialog>
    <v-dialog v-model="uploadOpen" persistent width="400">
      <v-card dark>
        <v-card-text>
          {{uploadRes}}
          <v-progress-linear indeterminate color="white" :width="10" v-if="isUploading"></v-progress-linear>
          <v-card-actions v-else>
            <v-btn outline color="white" @click="uploadOpen=false">确认</v-btn>
          </v-card-actions>
        </v-card-text>
      </v-card>
    </v-dialog>

  </div>
</template>
<script>
import {  mapState, mapGetters } from "vuex";
export default {
  components: {
    cropContent: () => import(/* webpackChunkName: 'crpoContent' */"@/components/user/cropContent.vue"),
    uploader: () => import(/* webpackChunkName: 'uploader' */"@/utils/uploader.vue")
  },
  data() {
    return {
      image: "",
      cropOpen: false,
      shadowOn: false,
      quality: "low",
      uploadOpen: false
    };
  },
  methods: {
    upload(file) {
      if(!file.target.files.length){
        return;
      }
      if (file.target.files[0].size > 3000000) {
        this.quality = "height";
      }
      if (file.target.files[0].size < 50000) {
        this.$store.commit('alerter/setMessage', "上传图片过小，请选择更清晰的照片。")
        return;
      }
      const reader = new FileReader();
      reader.onload = e => {
        this.image = e.target.result;
        this.shadowOn = false;
        this.cropOpen = true;
        file.target.value = "";
      };
      reader.onloadstart = function() {
        this.shadowOn = true;
      };
      reader.onabort = function() {
        this.$store.commit('alerter/setMessage', "读取中断。")
      };
      reader.onerror = function() {
        this.$store.commit('alerter/setMessage', "读取异常。")
      };
      reader.readAsDataURL(file.target.files[0]);
    },
    crop() {
      if (!this.photoBlob) {
        this.$store.commit('alerter/setMessage', "请先添加照片。")        
      } else {
        this.cropOpen = true;
      }
    },
    finishCrop() {
      this.cropOpen = false;
    },
    submit() {
      if (this.photoBlob) {
        let tempImage = new Image();
        tempImage.src = this.photoUrl;
        this.$store.dispatch("photo/uploadPhoto");
        this.uploadOpen = true;
      } else {
        this.$store.commit('alerter/setMessage', "请先添加照片。")        
      }
    },
    logout() {
      this.$store.commit("user/setLogout");
    }
  },
  computed: {
    ...mapState("photo", {
      photoBlob: "photoBlob",
      photoUrl: "photoUrl",
      isUploading: "isUploading",
      uploadRes: "uploadRes"
    }),
    ...mapGetters("photo", {
      message: "message"
    })
  },
  created() {
    if(!localStorage.getItem("token")) {
      this.$store.commit('alerter/setMessage', "请先登录。")
      this.$store.commit("user/setLogout");
      return;
    }
    this.$store.dispatch("photo/getPhoto");
  }
};
</script>
<style>
#photoArea {
    margin-top:5vh;width:100%;height:30vh;
    display:flex;
}
.shadow {
  height: 100vh;
  width: 100vw;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
  background-color: rgba(240, 248, 255, 0.603);
  text-align: center;
}
.shadow .loading {
  position: absolute;
  top: 50%;
  left: 50%;
  display: block;
  margin-left: -30px;
  margin-top: -30px;
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
#checkPage {
  width: 100vw;
  height: 100vh;
}
</style>
