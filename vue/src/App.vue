<template>
  <div v-if="loginStatus === 0" class="loginInterface">
    <login-interface></login-interface>
  </div>
  <div v-if="loginStatus === 1" class="anchorInterface">
    <anchor_interface></anchor_interface>
  </div>
  <div v-if="loginStatus === 2" class="chairmanInterface">

  </div>
</template>

<script>
import Anchor_interface from "@/components/anchor_interface.vue";
import LoginInterface from "@/components/login_interface.vue";

// define login status and identify
const OFF_LINE = 0;
const ANCHOR = 1;
const CHAIRMAN = 2;

export default {
  name: 'App',
  components: {LoginInterface, Anchor_interface},
  data() {
    return {
      // 登录状态
      loginStatus: OFF_LINE
    }
  }
}
</script>

<style scoped>

</style>
