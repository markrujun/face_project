<template>
    <v-dialog
      v-model="addSingleUserDialog"
      max-width="700"
    >
      <v-btn color="primary" slot="activator" >添加用户</v-btn>
      <v-card>
        
        <v-card-title class="headline">
          新增用户
          </v-card-title>
          <v-divider></v-divider>
        <v-container>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
            v-model="username"
            name="input-0"
            label="用户名"
            hint=""
            :rules="[value => !!value || '用户名不得为空.', ]"
          ></v-text-field>
            <v-text-field
            v-model="password"
            :append-icon="show ? 'visibility_off' : 'visibility'"
            :type="show ? 'text' : 'password'"
            name="input-1"
            label="密码"
            :rules="[value => !!value || '密码不得为空.', ]"
            :error="!passwordSame"
            :error-messages="warningMsg"
            @click:append="show = !show"
            counter
          ></v-text-field>
          <v-text-field
            v-model="againPassword"
            :append-icon="show1 ? 'visibility_off' : 'visibility'"
            :type="show1 ? 'text' : 'password'"
            name="input-2"
            :error="!passwordSame"
            :rules="[value => !!value || '请再次输入密码以确认', ]"
            :error-messages="warningMsg"
            label="确认密码"
            counter
            @click:append="show1 = !show1"
          ></v-text-field>
          <v-layout style="height:200px" row wrap>
            <v-flex xs6>
              <v-img contain max-height="200" :src="uploadPhoto" />
            </v-flex>
            <v-flex xs6>
              <uploader content="上传图片" icon="cloud_upload" :fab="false" @upload="handleUpload"/>
              <v-layout column  align-center>
                <v-btn v-if="uploadPhoto" @click="uploadPhoto=''" large color="error" ><v-icon >delete</v-icon> 清除图片</v-btn>
              </v-layout>
            </v-flex>
          </v-layout>
          <v-spacer></v-spacer>

          <v-btn
            color="primary darken-1"
            @click="comfirmAddSingle"
          >
            保存
          </v-btn>

          <v-btn
            color=" darken-1"
            @click="cancel"
          >
            取消
          </v-btn>
          </v-form>
        </v-container>
      </v-card>
    </v-dialog>
</template>
<script>
    export default {
        name: "auditorList",
        components: {
          uploader: () => import('@/utils/uploader.vue'),
        },
        data(){
            return {
                valid: true,
                addSingleUserDialog: false,
                uploadPhoto: '',
                username: '',
                password:'',
                againPassword: '',
                passwordSame:true,
                warningMsg:'',
                show: false,
                show1:false,
            }
        },
        watch: {
          againPassword(val) {
            if(val === this.password){
              this.passwordSame = true
              this.warningMsg = ""
            } else {
              this.passwordSame = false
              this.warningMsg = "两次密码输入不一致"
            }
          }
        },
        methods: {
            comfirmAddSingle() {
              if(this.$refs.form.validate()){
                if(!this.uploadPhoto){
                  this.$store.commit("alerter/setMessage","请上传图片");
                  return;
                }
                this.$store.dispatch('admin/addSingleUser', {username: this.username, password: this.password, photo: this.dataURItoBlob(this.uploadPhoto)})
                this.addSingleUserDialog = false
              }
            },
            dataURItoBlob(dataURI) {
                var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]; // mime类型
                var byteString = atob(dataURI.split(',')[1]); //base64 解码
                var arrayBuffer = new ArrayBuffer(byteString.length); //创建缓冲数组
                var intArray = new Uint8Array(arrayBuffer); //创建视图

                for (var i = 0; i < byteString.length; i++) {
                    intArray[i] = byteString.charCodeAt(i);
                }
                return new Blob([intArray], {type: mimeString});
            },
            handleUpload(value) {
              this.uploadPhoto = value
            },
            cancel() {
              this.addSingleUserDialog = false
              this.uploadPhoto = ''
              this.$refs.form.reset()
            }
            
        },
         
    }
</script>