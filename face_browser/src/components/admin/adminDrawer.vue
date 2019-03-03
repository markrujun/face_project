<template>
    <div>
        <v-navigation-drawer
      v-model="drawer"
      disable-resize-watcher
      fixed
      app
    >
      <v-list dense>
        <v-list-group v-for="(value, index) in navInfo" :key="index" value="false" no-action>
            <v-list-tile slot="activator">
              <v-list-tile-action>
                <v-icon>{{value.icon}}</v-icon>
              </v-list-tile-action>
              <v-list-tile-title>{{value.title}}</v-list-tile-title>
            </v-list-tile>
            <v-list-tile v-for="(i, ind) in value.child" :key="ind" :to="i.to">
              <v-list-tile-title v-text="i.name" />
            </v-list-tile>
          </v-list-group>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar color="indigo" dark fixed app>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
       <v-toolbar-title>Application</v-toolbar-title>
    </v-toolbar>
    </div>
</template>
<script>
    export default {
        name: 'adminDrawer',
        data() {
            return {
                drawer: null,
                navInfo: [
                  {
                    title: "照片审核",
                    icon: "account_circle",
                    child: [
                      {
                        to: "checkList",
                        name: "审核列表"
                      },
                      {
                        to: "photoList",
                        name: "所有图片"
                      },
                    ]
                  },
                  {
                    title: "用户",
                    icon: "account_circle",
                    child: [
                      {
                        to: "userList",
                        name: "用户列表"
                      },
                      {
                        to: "adminList",
                        name: "管理员列表"
                      },
                    ]
                  },
                  {
                    title: "系统",
                    icon: "home",
                    child: [
                      {
                        to: "systemConfig",
                        name: "系统变量"
                      }
                    ]
                  }
                ]
            }
        }
    }
</script>
