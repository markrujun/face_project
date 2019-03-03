<template>
  <v-container>
    <v-card style="width: 100%">
      <v-card-title primary-title>
        <div>
          <h3 class="headline mb-0">系统配置</h3>
        </div>
      </v-card-title>
      <v-divider></v-divider>
      <v-container>
        <v-layout row wrap>
          <v-flex v-for="(value, key) in configList" :key="key" xs4>
            <label>{{key}}</label>
            <v-text-field style="margin:10px 50px 20px 0;" :label="key" :prefix="value.prefix" :suffix="value.suffix" :rules="value.rules" v-model="configData[value.value]" outline></v-text-field>
          </v-flex>
        </v-layout>
      </v-container>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :disabled="hasChanged" @click="saveConfig" color="primary">保存</v-btn>
        <v-btn :disabled="hasChanged" @click="cancelChange">取消</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
<script>
import { mapState } from 'vuex'
export default {
  name: "systemConfig",
  data() {
    return {
      configList: {
        "系统域名": {
          value: 'host',
          prefix: '',
          suffix: '',
          message: '请填写完整的域名，如https://XXXX.XX',
          rules: [value => !!value || '不得为空.', value => {
            const patternURL = /https?:\/\/[a-z0-9_.:]+\/[-a-z0-9_:@&?=+,.!/~*%$]*(\.(html|htm|shtml))?/
            return patternURL.test(value) || 'Invalid URL.'
          }]

        },
        "照片长度": {
          value: 'photoLength',
          prefix: '',
          suffix: 'PX',
          message: '采集照片的长度，单位（像素）',
          rules: [value => !!value || '不得为空.', ]

        },
        "照片宽度": {
          value: 'photoWidth',
          prefix: '',
          suffix: 'PX',
          message: '采集照片的宽度，单位（像素）',
          rules: [value => !!value || '不得为空.', ]

        },
        "储存文件夹": {
          value: 'dir',
          prefix: '/',
          suffix: '',
          message: '照片储存的相对路径，可将不同年份照片储存在不同文件夹',
          rules: [value => !!value || '不得为空.', ]

        },
        "照片格式": {
          value: 'photoFormat',
          prefix: '.',
          suffix: '',
          message: '照片储存格式',
          rules: [value => !!value || '不得为空.', ]

        },
        "成功置信度": {
          value: 'confidence',
          prefix: '',
          suffix: '%',
          message: '人脸识别通过的置信度',
          rules: [value => !!value || '不得为空.', ]

        },
      },
      configData: {
        host: null,
        photoLength: null,
        photoWidth: null,
        photoFormat: null,
        dir: null,
        confidence: null,
      }
    }
  },
  methods: {
    initConfigList() {
      this.configList = Object.assign({}, this.configList);
    },
    saveConfig() {
      this.$store.dispatch('admin/saveConfig', { configData: this.configData })
    },
    cancelChange() {
      this.configData = Object.assign({}, this.$store.state.admin.configs)
    }
  },
  computed: {
    hasChanged() {
      for (let key in this.configData) {
        if (this.configData[key] !== this.$store.state.admin.configs[key]) {
          return false
        }
      }
      return true
    },
  },
  mounted() {
    this.initConfigList();

    this.$store.dispatch('admin/getConfig').then((data) => {
      this.configData = data
    });
  }
}
</script>