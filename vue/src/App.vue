<template>
  <div id="app"><router-view></router-view></div>
</template>

<script>
import Anchor_interface from "@/components/anchor_interface.vue";
import LoginInterface from "@/components/login_interface.vue";
import Cookies from 'js-cookie'
import Chairman_interface from "@/components/chairman_interface.vue";
import {router} from "@/plugins/router";

// define login status and identify
const OFF_LINE = 0;
const ANCHOR = 1;
const CHAIRMAN = 2;

export default {
  name: 'App',
  components: {Chairman_interface, LoginInterface, Anchor_interface},
  watch: {
    loginStatus(val) {
      if (val === OFF_LINE)
        this.account = ''
      else
        this.account = Cookies.get('account')
    }
  },
  mounted() {
    if (Cookies.get('account') !== undefined) {
      this.account = Cookies.get('account')
      this.loginStatus = Cookies.get('type') === 'anchor' ? ANCHOR : CHAIRMAN
      router.push('/interface/' + Cookies.get('type'))
    }
    else {
      router.push('/interface/login')
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
