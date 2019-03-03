<template>
    <v-container>        
        <v-card style="width: 100%"> 
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">用户列表</h3>
          </div>
        </v-card-title>
        <v-divider></v-divider>
        <v-container>
            <v-text-field
                v-model="search"
                append-icon="search"
                label="Search"
                single-line
                hide-details
            ></v-text-field>
            <v-data-table
                :headers="headers"
                :items="desserts"
                item-key="name"
                class="elevation-1"
                :search="search"
            >
                <template slot="items" slot-scope="props">
                <td>{{ props.item.username }}</td>
                <td> <v-img width="70" :src="props.item.photoUrl"></v-img> </td>
                <td >
                    <v-icon
                        small
                        class="mr-2"
                        @click="edit(props.item)"
                    >
                        edit
                    </v-icon>
                    <v-icon
                        small
                        class="mr-2"
                        @click="deleteIt(props.item)"
                    >
                        delete
                    </v-icon>
                    </td>
                </template>
                <template slot="footer">
                <td  :colspan="headers.length">
                    <addSingleUserDialog />
                    <v-btn color="primary" to="addUsers"> 批量添加</v-btn>
                </td>
                </template>
            </v-data-table>
        </v-container>
      </v-card>
      <v-dialog
      v-model="delDialog"
      max-width="290"
    >
      <v-card>

        <v-card-text>
          确定要删除该用户吗？
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="primary darken-1"
            @click="sureDelete"
          >
            确认
          </v-btn>

          <v-btn
            color=" darken-1"
            @click="delDialog = false"
          >
            取消
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="editDialog"
      max-width="500"
    >
      <v-card>

        <v-card-title class="headline">
          修改用户信息
          </v-card-title>
          <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="primary darken-1"
            @click=""
          >
            保存
          </v-btn>

          <v-btn
            color=" darken-1"
            @click=""
          >
            取消
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    </v-container>
</template>
<script>
    export default {
        name: "auditorList",
        components: {
          uploader: () => import(/* webpackChunkName: 'uploader' */'@/utils/uploader.vue'),
          addSingleUserDialog: () => import(/* webpackChunkName: 'addSingleUser' */'./addSingleUserDialog.vue'),
          addUsersDialog: () => import(/* webpackChunkName: 'addUsers' */'./addUsers.vue'),
        },
        data(){
            return {
                delDialog: false,
                editDialog: false,
                search: '',
                headers: [
                {
                    text: '用户名',
                    align: 'left',
                    sortable: false,
                    value: "username"
                },
                { text: '照片',sortable: false, value: 'photoUrl' },
                { text: '编辑',sortable: false, },
                
                ],
            }
        },
        computed: {
          desserts: {
            get: function() {
              return this.$store.state.admin.userList
            },
            set: function(val) {
            }
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
            deleteIt(item) {
                this.deleteItem = item
                this.delDialog = true
            },
            edit(item) {
                this.editItem = item
                this.editDialog = true
            },
            sureDelete(){
                this.$store.dispatch('admin/deleteUser', {username: this.deleteItem.username});
                this.delDialog = false                
            },
            addSingleUser() {
              this.addSingleUserDialog = true
            },
            addUsers() {
              
            },
            comfirmAddSingle() {
              if(this.$refs.form.validate()){
                this.$store.dispatch('admin/addSingleUser', {username: this.username, password: this.password, photo:this.uploadPhoto})
              }
            },
            handleUpload(value) {
              this.uploadPhoto = value
            }
        },
        mounted() {
          this.$store.dispatch('admin/getUserList')
        }
    }
</script>