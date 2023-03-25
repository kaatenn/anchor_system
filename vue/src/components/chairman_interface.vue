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
            <p>管理主播</p>
          </el-menu-item>
          <el-menu-item index="2">
            <el-icon><Service /></el-icon>
            <p>签约主播</p>
          </el-menu-item>
          <el-menu-item index="3">
            <el-icon><Bell /></el-icon>
            <p>签约请求</p>
          </el-menu-item>
          <el-menu-item index="4">
            <el-icon>
              <UserFilled/>
            </el-icon> <!--UserFilled has defined in element-plus-->
            <p>账户设置</p>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!---------main----------->
      <el-container v-loading="loading">
        <el-main>
          <!------------page1--------------->
          <div v-if="page === '1'">
            <el-table :data="employed_info" stripe style="width: 100%">
              <el-table-column label="账号" width="160">
                <template #default="scope">
                  <p> {{ scope.row.anchor_account }} </p>
                </template>
              </el-table-column>
              <el-table-column label="昵称" width="160">
                <template #default="scope">
                  <p> {{ scope.row.anchor_nickname }} </p>
                </template>
              </el-table-column>
              <el-table-column label="工作状态" width="160">
                <template #default="scope">
                  <p style="color: #b3e19d" v-if="scope.row.working_status">直播中</p>
                  <p style="color: #F56C6C" v-if="!scope.row.working_status">未开播</p>
                </template>
              </el-table-column>
              <el-table-column label="直播进度" width="240">
                <template #default="scope">
                  <el-progress :percentage="parseFloat(scope.row.working_time_percent)" />
                </template>
              </el-table-column>
              <el-table-column label="可执行操作" width="160">
                <template #default="scope">
                  <el-button type="danger" @click="handleDismiss(scope.row.anchor_account)">解雇</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <!------------page2--------------->
          <div v-if="page === '2'">

          </div>
          <!------------page3--------------->
          <div v-if="page === '3'">

          </div>
          <!------------page3--------------->
          <div v-if="page === '4'">
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
import {httpDelete, httpGet, httpPost} from "@/plugins/axios";
import {attr_name, attr_name_cn} from "@/plugins/utils";
import {ElMessage} from "element-plus";
import {router} from "@/plugins/router";
import Cookies from "js-cookie";

export default {
  name: "chairman_interface",

  data() {
    return {
      loading: true,
      page: '1',
      account: '',
      employed_info: [
        {
          anchor_account: '',
          anchor_nickname: '',
          working_status: '',
          working_time_percent: '0'
        }
      ],
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
    this.loading = true
    if (this.account === '') {
      if (Cookies.get('account') === '') {
        router.push('/interface/login')
      } else {
        this.account = Cookies.get('account')
      }
    }
    this.getUserInfo()
    this.getEmployedAnchor()
    this.loading = false
  },

  methods: {
    selectHandler(index) {
      this.page = index
    },
    handleEdit(index) {
      this.is_edit[index] = true
    },
    async handleSave(index) {
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

      await httpGet.get('/token')

      await httpPost.post('/updateInfo', params)
          .then(() => {
            this.is_edit[index] = false
            this.loading = true
            this.getUserInfo()
            this.loading = false
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
    async handleDismiss(anchor_account) {
      let params = new URLSearchParams()

      params.append('anchor_account', anchor_account)
      params.append('conference_account', this.account)

      await httpGet.get('/token')

      await httpDelete.delete('/dismiss', {data: params})
          .then(res => {
            this.loading = true
            this.getEmployedAnchor()
            this.loading = false
            console.log(res)
          })
    },
    async getUserInfo() {
      await httpGet.get('/getUserInfo?type=chairman&account=' + this.account)
          .then(res => {
            this.user_info = res.data
          })
          .catch(err => {
            console.log(err)
          })
    },
    async getEmployedAnchor() {
      let params = new URLSearchParams()

      params.append('account', this.account)

      await httpGet.get('/token')

      await httpPost.post('/getEmployedAnchor', params)
          .then(res => {
            this.employed_info = res.data
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