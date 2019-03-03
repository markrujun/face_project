<template>
  <v-container>
      <v-card style="width:100%">
        <v-card-title class="headline">
          批量添加
          </v-card-title>
          <v-divider></v-divider>
        <v-container>
          <v-btn><v-icon>cloud_upload</v-icon><label for="excelInput">上传EXCEL</label></v-btn>
          <input style="display:none" type="file" name="excelInput" id="excelInput" @change="uploadExcel" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" >
          <v-dialog 
          v-model="viewDataDialog"
          max-width="700"> 
            <a color="primary" slot="activator" >预览</a>
          <v-card>
            <v-container>
            <v-data-table
                :headers="tableData.header"
                :items="tableData.data"
                item-key="name"
                class="elevation-1"
            >
                <template slot="items" slot-scope="props">
                  <td v-for="(i,j) in tableData.header" :key="j">{{props.item[i["value"]]}}</td>
                </template>
            </v-data-table>
        </v-container>
          </v-card>
          </v-dialog> {{tableData.data.length ? `${tableData.data.length}条记录`: ''}} <a color="primary" :href="mobanUrl" >  下载模板</a>
          <br>
          <v-btn><v-icon>cloud_upload</v-icon><label for="zipInput">图片压缩包</label></v-btn>{{zip.name? `${zip.name}(${zip.size})`:''}}
          <p>注:请上传格式为rar或zip的压缩包 </p>
          <input style="display:none" type="file" name="zipInput" id="zipInput" @change="uploadZip" accept="application/zip" >
          
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="submitAddUsers" color="primary">保存</v-btn>
          <v-btn to="userList">返回</v-btn>
        </v-card-actions>
      </v-card>
      <v-dialog v-model="isExporting" persistent width="400">
      <v-card dark>
        <v-card-text>
          正在上传，请等待...
          <v-progress-linear indeterminate></v-progress-linear>
          <v-card-actions >
            <v-spacer></v-spacer>
            <v-btn v-if="isExporting" outline color="white" @click="isExporting =false">取消</v-btn>
          </v-card-actions>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog v-model="resultDialog" persistent width="500">
      <v-card>
        <v-card-title primary-title> <h3>上传结果</h3></v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <h4>上传完成，上传记录{{successList.length + failedList.length}}条, 成功{{successList.length}}, 失败{{failedList.length}}。</h4>
          <div v-if="failedList.length > 0">
            <h4>未成功学号：</h4>
            <h4 v-for="i in failedList" :key="i"> {{i}} </h4>
          </div>
          <v-card-actions >
            <v-spacer></v-spacer>
            <v-btn  to="userList">确定</v-btn>
          </v-card-actions>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script>
 import XLSX from 'xlsx';
    export default {
        name: "auditorList",
        components: {
          uploader: () => import('@/utils/uploader.vue'),
        },
        data(){
            return {
              mobanUrl: 'http://127.0.0.1:5000/static/testUsers.xlsx',
              viewDataDialog: false,
              isExporting: false,
              tableData: {
                header: [

                ],
                data:[

                ]
              },
              zip: {
                name: '',
                size: '',
                data: ''
              },
              successList:[],
              failedList:[]
            }
        },
        watch: {
        },
        methods: {
            uploadExcel(val) {
              const file = val.srcElement.files[0]
              const reader = new FileReader()
              const _this = this
              reader.readAsBinaryString(file)
              reader.onload = function(e) {
                const data = e.target.result;
                const EXCEL = XLSX.read(data, {
                  type: 'binary'
                })
                _this.tableData = _this.formateSheet(EXCEL)
                _this.addSingleUserDialog = true
              }
            },
            formateSheet(data) {
              let resultData = {header: [], data: []}
              const first_sheet_name = data.SheetNames[0];
              /* Get worksheet */
              const worksheet = data.Sheets[first_sheet_name];
              /* size = ["A1", "C28"] */
              const size = data.Sheets[first_sheet_name]["!ref"].split(':')
              const col = [size[0].substr(0,1), size[1].substr(0,1)]
              const coln = col[1].charCodeAt(0) - col[0].charCodeAt(0) + 1
              const cols = []
              for(let i=0;i<coln;i++) {
                cols.push(String.fromCharCode(col[0].charCodeAt(0)+i))
              }
              const row = [size[0].substr(1,size[0].length - 1), size[1].substr(1,size[1].length - 1)]
              const rown = parseInt(row[1]) - parseInt(row[0]) + 1

              for(let i in cols){
                // Add header
                resultData.header.push({
                  text: worksheet[cols[i]+(parseInt(row[0]))].v,
                  value: worksheet[cols[i]+(parseInt(row[0]))].v
                })
                // add data
                for(let j=1;j<rown;j++) {
                  if(i==0){
                    resultData.data.push({})
                  }
                }
              }
              return resultData
            },
            uploadZip(val) {
              const file = val.srcElement.files[0]
              const reader = new FileReader()
              const _this = this
              this.zip = {
                size : file.size,
                name: file.name
              }
              reader.readAsArrayBuffer(file)
              reader.onload = function(e) {
                const data = e.target.result;
                _this.zip.data = data
              }
            },
            submitAddUsers(){
              this.isExporting = true
              this.$store.dispatch('admin/addUsers', {data: this.tableData.data, zipFile: this.zip.data}).then((result)=> {
                this.isExporting = false
                this.resultDialog = true
                this.successList = result.successList
                this.failedList = result.failedList
              })
            }
            
        },
    }
</script>