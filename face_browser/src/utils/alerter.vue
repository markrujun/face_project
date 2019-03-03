<template>
      <v-snackbar
      v-model="show1"
      :timeout="timeout"
      top
    >
      {{ message }}
      <v-btn
        color="pink"
        flat
        @click="close"
      >
        <v-icon>close</v-icon>
      </v-btn>
  </v-snackbar>
</template>
<script>
import { mapState } from 'vuex'

export default {
    data() {
        return {
            timeout: 3500,
            show1: false
        }
    },
    computed: {
        ...mapState("alerter", {
            message: "message",
            show: "show"
        }),
    },
    methods: {
        close(){
            this.show1 = false
        }
    },
    watch: {
        show() {
            this.show1 = true 
        }
    }
}
</script>

