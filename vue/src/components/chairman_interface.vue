<template>
  <el-container>
    <!--------------------------------header-------------------------------->
    <el-header style="background-color: #E6E6FA; line-height: 150px; font-size: xx-large; color: #606266"
               height="150px">
      Anchor Certain（公会端）
    </el-header>


    <!-------------aside--------------->
    <el-container>
      <el-aside width="200px">
        <el-menu
            active-text-color="#DA70D6"
            default-active="1"
            text-color="#606266"
            @select="selectHandler">
          <el-menu-item index="1">
            <el-icon>
              <Grid/>
            </el-icon> <!--Grid has defined in element-plus-->
            <p>签约主播</p>
          </el-menu-item>
          <el-menu-item index="2">
            <el-icon>
              <UserFilled/>
            </el-icon> <!--UserFilled has defined in element-plus-->
            <p>账户信息</p>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!---------main----------->
      <el-container>
        <el-main>
          <div v-if="page === '1'">

          </div>
          <div v-if="page === '2'">

            {{ account }}
          </div>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import {httpGet} from "@/plugins/axios";

export default {
  name: "chairman_interface",

  data() {
    return {
      page: '1',
      userInfo: {
        nickName: '',
        sex: '',
        telephoneNumber: '',
        introduction: ''
      }
    }
  },

  props: {
    account: String
  },

  watch: {
    account(val) {
      console.log(val)
    }
  },

  mounted() {
    this.getUserInfo()
  },

  methods: {
    selectHandler(index) {
      this.page = index
    },
    getUserInfo() {
      httpGet.get('/getUserInfo?type=chairman&account=' + this.account)
          .then(res => {
            this.userInfo = res.data
          })
          .catch(err => {
            console.log(err)
          })
    }
  }
}
</script>

<style scoped>

</style>