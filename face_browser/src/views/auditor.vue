<template>
  <v-app>
    <v-content>
        <v-layout>
          <transition>
            <router-view></router-view>            
          </transition>
          <alerter />
        </v-layout>
    </v-content>
  </v-app>
</template>

<script>
  export default {
    components: {
      alerter: () => import(/* webpackChunkName: 'alerter' */'@/utils/alerter.vue'),
    }
  }
</script>
