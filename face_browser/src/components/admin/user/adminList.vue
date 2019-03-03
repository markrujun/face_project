<template>
    <v-container>        
        <v-card style="width: 100%"> 
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">管理员列表</h3>
          </div>
        </v-card-title>
        <v-divider></v-divider>
        <v-container>
            <v-data-table
                :headers="headers"
                :items="desserts"
                item-key="name"
                class="elevation-1"
            >
                <template slot="items" slot-scope="props">
                <td>{{ props.item.adminname }}</td>
                <td>{{ props.item.permission }}</td>
                <td >
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
                    <addAdminDialog />
                </td>
                </template>
            </v-data-table>
        </v-container>
        <v-dialog
      v-model="deleteDialog"
      max-width="290"
    >
      <v-card>

        <v-card-text>
          确定要删除该管理员——{{deleteItem.adminname}}吗？
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
            @click="deleteDialog = false"
          >
            取消
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
      </v-card>
    </v-container>
</template>
<script>
    export default {
        name: "adminList",
        components: {addAdminDialog: () => import(/* webpackChunkName: 'adminDialog' */'./addAdmin.vue') },
        data(){
            return {
                headers: [
                {
                    text: '管理员名',
                    align: 'left',
                    sortable: false,
                    value: "adminname"
                },
                { text: '权限',sortable: false, value: 'permission' },
                { text: '编辑',sortable: false, },
                
                ],
                deleteDialog: false,
                deleteItem: ''
            }
        },
        methods: {
            addUser() {

            },
            deleteIt(val) {
                this.deleteDialog = true
                this.deleteItem = val
            },
            sureDelete() {
                this.$store.dispatch('admin/deleteAdmin', {adminname: this.deleteItem.adminname})
                this.deleteDialog = false
            }
        },
        computed: {
          desserts: {
            get: function() {
              return this.$store.state.admin.adminList
            },
            set: function(val) {
            }
          }
        },
        created() {
            this.$store.dispatch('admin/getAdminList')
        }
    }
</script>