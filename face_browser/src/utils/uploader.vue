<template>
  <v-layout column align-center>
    <v-btn :fab="fab" large color="transparent">
      <label style="height:72px;width:72px;display:block;border-radius: 50%;" for="imageInput">
        <v-icon dark> {{icon}} </v-icon> {{content}}
      </label>
    </v-btn>
    <input @change="upload" type="file" accept="image/*" id="imageInput" style="display:none" name="imageInput">
  </v-layout>
</template>
<script>
    export default {
      props:{
          icon: {
              required: true
          },
          content: {
              default:''
          },
          fab: {
              default: true
          }
      },
      data() {
        return {

        }
      },
      methods: {
          upload(file) {
            if (!file.target.files.length) {
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
            this.$emit("upload",e.target.result);
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
      }
    }
</script>
