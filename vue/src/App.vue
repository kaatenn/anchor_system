<template>
  <div v-if="loginStatus === 0" class="loginInterface">
    <login-interface @login = "changeLoginStatus"></login-interface>
  </div>
  <div v-if="loginStatus === 1" class="anchorInterface">
    <anchor_interface></anchor_interface>
  </div>
  <div v-if="loginStatus === 2" class="chairmanInterface">
    chairmanInterface
  </div>
</template>

<script>
import Anchor_interface from "@/components/anchor_interface.vue";
import LoginInterface from "@/components/login_interface.vue";
import Cookies from 'js-cookie'

// define login status and identify
const OFF_LINE = 0;
const ANCHOR = 1;
const CHAIRMAN = 2;

export default {
  name: 'App',
  components: {LoginInterface, Anchor_interface},
  mounted() {
    if (Cookies.get('account') !== undefined) {
      this.account = Cookies.get('account')
      this.loginStatus = Cookies.get('type') === 'anchor' ? ANCHOR : CHAIRMAN
    }
  },
  data() {
    return {
      // 登录状态
      loginStatus: OFF_LINE,
      account: ''
    }
  },
  methods: {
    changeLoginStatus(status) {
      this.loginStatus = status
    }
  }
}
</script>

<style scoped>

</style>
