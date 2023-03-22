<template>
  <el-container>
    <!--------------------------------header-------------------------------->
    <el-header style="background-color: #E6E6FA; line-height: 150px; font-size: xx-large; color: #606266"
               height="150px">
      Anchor Certain（公会端）
    </el-header>

    <el-container>
      <!-------------aside--------------->
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
          <!------------page1--------------->
          <div v-if="page === '1'">

          </div>
          <!------------page2--------------->
          <div v-if="page === '2'">
            <span style="font-size: xx-large; margin-bottom: 20px; color: #909399">{{ account }}</span>
            <el-table :data="user_info" style="width: 100%">
              <el-table-column label="设置项" width="180" prop="name"></el-table-column>
              <el-table-column label="内容" width="400">
                <template #default="scope">
                  <span v-if="!is_edit[scope.$index]">{{ scope.row.attributes }}</span>
                  <el-input v-if="is_edit[scope.$index] && scope.$index !== 1" v-model="scope.row.attributes"
                            placeholder="请输入内容"></el-input>
                  <el-radio-group v-model="scope.row.attributes" v-if="is_edit[scope.$index] && scope.$index === 1 ">
                    <el-radio label="男">男</el-radio>
                    <el-radio label="女">女</el-radio>
                  </el-radio-group>
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template #default="scope">
                  <el-button v-if="!is_edit[scope.$index]" size="small" @click="handleEdit(scope.$index, scope.row)">
                    编辑
                  </el-button>
                  <el-button v-if="is_edit[scope.$index]" size="small" @click="handleSave(scope.$index, scope.row)">
                    保存
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div style="text-align: center; width: 50%">
              <el-button type="danger" @click="handleSignOut">注销</el-button>
            </div>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import {httpGet, httpPost} from "@/plugins/axios";
import {attr_name, attr_name_cn} from "@/plugins/utils";
import {ElMessage} from "element-plus";
import {router} from "@/plugins/router";
import Cookies from "js-cookie";

export default {
  name: "chairman_interface",

  data() {
    return {
      page: '1',
      account: '',
      is_edit: [false, false, false, false],
      user_info: [
        {name: '昵称', attributes: ''},
        {name: '性别', attributes: ''},
        {name: '电话号码', attributes: ''},
        {name: '简介', attributes: ''},
      ]
    }
  },

  watch: {},

  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.account = to.params.account
    })
  },

  mounted() {
    if (this.account === '') {
      if (Cookies.get('account') === '') {
        router.push('/interface/login')
      } else {
        this.account = Cookies.get('account')
      }
    }
    this.getUserInfo()
  },

  methods: {
    selectHandler(index) {
      this.page = index
    },
    getUserInfo() {
      httpGet.get('/getUserInfo?type=chairman&account=' + this.account)
          .then(res => {
            this.user_info = res.data
          })
          .catch(err => {
            console.log(err)
          })
    },
    handleEdit(index) {
      this.is_edit[index] = true
    },
    handleSave(index) {
      let params = new URLSearchParams()

      /* check if the info input is legal*/

      if (this.user_info[index].attributes === '') {
        ElMessage.error('请输入' + attr_name_cn[index])
        return
      }

      if (index === 1) {
        if (this.user_info[0].attributes.length > 10) {
          ElMessage.error('昵称长度应小于 10')
          return
        }
      }

      if (index === 2) {
        if (this.user_info[2].attributes.length !== 11) {
          ElMessage.error('电话号码长度应为 11')
          return
        }
      }

      if (index === 3) {
        if (this.user_info[3].attributes.length > 255) {
          ElMessage.error('简介长度应不超过 255')
          return
        }
      }

      params.append('type', 'chairman')
      params.append('account', this.account)
      params.append('attr_name', attr_name[index])
      if (index !== 1) {
        params.append('attributes', this.user_info[index].attributes)
      } else {
        if (this.user_info[index].attributes === '男') {
          params.append('attributes', '0')
        } else {
          params.append('attributes', '1')
        }
      }

      httpGet.get('/token')

      httpPost.post('/updateInfo', params)
          .then(res => {
            this.is_edit[index] = false
            this.getUserInfo()
            console.log(res)
          })
          .catch(err => {
            console.log(err)
          })
    },
    handleSignOut() {
      Cookies.remove('account')
      Cookies.remove('type')
      router.push('/interface/login')
    },
    getEmployedAnchor() {
      let params = new URLSearchParams()

      params.append()

      httpGet.get('/token')

      httpPost.post('/getEmployedAnchor', )
    }
  }
}
</script>

<style scoped>

</style>