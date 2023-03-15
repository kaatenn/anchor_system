<template>
  <el-container>
    <el-header style="background-color: #E6E6FA; line-height: 200px; font-size: xx-large" height="200px">
      Anchor Certain
    </el-header>
    <el-container>
      <el-aside width="200px">
        <el-menu
          active-text-color="#DA70D6"
          background-color="#5F9EA0"
          default-active="1"
          text-color="#fff"
          @select="selectHandler">

        </el-menu>
      </el-aside>
      <el-container>
        <el-main>Main</el-main>
        <el-footer>Footer</el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import {httpGet} from "@/plugins/axios";

export default {
  name: "anchor_interface",
  data() {
    return {

    }
  },

  props: {
    account: String
  },

  watch: {
    account(val) {
      httpGet.get('/getUserInfo?account=' + val)
    }
  },

  methods: {
    selectHandler() {

    }
  }
}
</script>

<style scoped>

</style>