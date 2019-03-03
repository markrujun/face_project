<template>
  <v-app style="width:100%">
    <admin-drawer />
    <v-container>
      <v-layout justify-center>
        <router-view></router-view>
      </v-layout>
    </v-container>
    <v-footer color="indigo" app>
      <span class="white--text">&copy; 2017</span>
    </v-footer>
    <admin-login />
  </v-app>
</template>

<script>
  export default {
      components: {
          adminDrawer: () => import(/* webpackChunkName: 'adminDrawer' */'@/components/admin/adminDrawer.vue'),
          adminLogin: () => import(/* webpackChunkName: 'adminLogin' */'@/components/admin/adminLogin.vue'),
      },
  }
</script>