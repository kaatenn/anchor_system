<template>
  <el-container>
    <!--------------------------------header-------------------------------->
    <el-header style="background-color: #E6E6FA; line-height: 200px; font-size: xx-large" height="200px">
      Anchor Certain
    </el-header>


    <!-------------aside--------------->
    <el-container>
      <el-aside width="200px" >
        <el-menu
          active-text-color="#DA70D6"
          default-active="1"
          text-color="#fff"
          @select="selectHandler">
          <el-menu-item index="1">
            <el-icon><Grid /></el-icon> <!--Grid has defined in element-plus-->
            <p>签约公会</p>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!---------main----------->
      <el-container>
        <el-main>

        </el-main>
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
      associations: []
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