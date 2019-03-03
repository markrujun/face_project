
<template>
<div style="width: 100%;">
    <v-card style="padding:20px 30px;;"> 
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">审核列表  </h3>
          </div>
        </v-card-title>
    <v-text-field
        v-model="search"
        append-icon="search"
        label="Search"
        single-line
        hide-details
        ></v-text-field>
  <v-data-table
    v-model="selected"
    :headers="headers"
    :items="desserts"
    item-key="name"
    select-all
    class="elevation-1"
    :search="search"
    ref="table"
  >
    <template slot="items" slot-scope="props" >
      <td>
        <v-checkbox
          v-model="props.selected"
          primary
          hide-details
        ></v-checkbox>
      </td>
      <td>{{ props.item.username }}</td>
      <td>{{ props.item.name }}</td>
      <td><img width="70" :src="props.item.systemPhoto"></td>
      <td><img :ref="props.item.name" width="70" :src="props.item.uploadPhoto"></td>
      <td>{{ props.item.confidence }}</td>
      <td>{{ props.item.status }}</td>
      <td>{{ props.item.time }}</td>
      <td>{{ props.item.auditor }}</td>
      <td>{{ props.item.remark }}</td>
      <td >
          <v-icon
            small
            class="mr-2"
            @click="editItem(props.item)"
          >
            edit
          </v-icon>
        </td>
    </template>
    <template slot="footer">
      <td :colspan="headers.length+1">
        <v-btn :disabled="isExporting" @click="exportPhoto">导出所选图片</v-btn>
      </td>
    </template>
  </v-data-table>
  <v-dialog v-model="editOpen" persistent max-width="500">
      <v-card>
        <v-card-title class="headline">修改审核</v-card-title>
        <v-select
            style="margin:15px 60px;"
            :items="selectItems"
            v-model="selectedStatus"
            label="请选择状态"
        ></v-select>
        <v-text-field style="margin:15px 60px;" v-model="remark" label="备注" required></v-text-field>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat @click="editOpen = false">取消</v-btn>
          <v-btn color="green darken-1" flat @click="submitEdit">确认</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="isExporting" persistent width="400">
      <v-card dark>
        <v-card-text>
          {{exportProgess <= 100 ? `正在下载图片  `+DownClassObj.finishLength + "/" + selected.length : "正在打包"}}
          <v-progress-linear v-model="exportProgess"></v-progress-linear>
          <v-card-actions >
            <v-spacer></v-spacer>
            <v-btn v-if="isExporting" outline color="white" @click="calcelExport">取消</v-btn>
          </v-card-actions>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-card>
  </div>
</template>
<script>
import { DownClass } from '@/utils/DownClass'
import { mapState } from 'vuex';
  export default {
    name: "checkList",
    data() {
      return {
        selected: [],
        selectedItem:{},
        selectedStatus:'',
        isExporting: false,
        DownClassObj: {
          toZipLock: false
        },
        search: '',
        editOpen: false,
        remark: '',
        exportProgess:0,
        valueDeterminate: 50,
        selectItems: [
            '待审核(2)',
            '未通过(3)',
            '审核通过(4)',
        ],
        headers: [
          {
            text: '学号',
            align: 'left',
            sortable: false,
            value: "stuid"
          },
          { text: '姓名', value: 'name' },
          { text: '系统照片', value: 'systemPhoto' },
          { text: '上传照片', value: 'upLoadPhoto' },
          { text: '置信度', value: 'confidence' },
          { text: '状态', value: 'status' },
          { text: '时间', value: 'time' },
          { text: '审核员', value: 'auditor' },
          { text: '备注', value: 'remark'},
          { text: '修改状态', },
          
        ],
      }
    },
    methods: {
        editItem(item) {
          this.selectedItem = item
          this.editOpen = true
        },
        submitEdit() {
          this.$store.dispatch('admin/editCheckItem', {username: this.selectedItem.username,status: this.selectedStatus[this.selectedStatus.length-2], remark: this.remark})
          this.editOpen = true
          this.selectedItem = {}
        },
        exportPhoto() {
          this.DownClassObj = new DownClass()
          let fileArray = []
          if(this.selected.length === 0) {
            this.$store.commit('alerter/setMessage', "请先选择图片！")
            return 
          }
          this.isExporting = true
          this.selected.map(item => {
            fileArray.push({
              lock:false,
              fullName:item.name,
              url:item.uploadPhoto,
              blob: null
            })
          })
            // 传入需要下载图片列表数组
            this.DownClassObj.queue = fileArra
            // 触发下载打包(是一个异步进程)
            // 通过 `toZipLock` 属性是否已经打包完成
            this.DownClassObj.toZip('zipName').then(res => {
              this.isExporting = false              
            })
            
        },
        calcelExport() {
          this.DownClassObj.clearImages()
          this.isExporting = false
        }
    },
    watch: {
      DownClassObj: {
        handler(val) {
          this.exportProgess = val.finishLength/val.queue.length * 100
        },
        deep: true
      }
    },
    mounted() {
      this.$store.dispatch('admin/getCheckList')
    },
    computed: {
      ...mapState('admin', {
        desserts: "checkList"
      })
    }
  } 
</script>