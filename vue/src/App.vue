<template>
  <div v-if="loginStatus === 0" class="loginInterface">
    <login-interface @login="changeLoginStatus"></login-interface>
  </div>
  <div v-if="loginStatus === 1" class="anchorInterface">
    <anchor_interface :account="account"></anchor_interface>
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
  watch: {
    loginStatus(val) {
      if (val !== OFF_LINE)
        this.account = ''
      else
        this.account = Cookies.get('account')
    }
  },
  mounted() {
    if (Cookies.get('account') !== undefined) {
      this.account = Cookies.get('account')
      this.loginStatus = Cookies.get('type') === 'anchor' ? ANCHOR : CHAIRMAN
    }
  },
  data() {
    return {
      loginStatus: OFF_LINE, // loginStatus can also mean user type
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
