<template>
  <el-container>
    <!--------------------------------header-------------------------------->
    <el-header style="background-color: #E6E6FA; line-height: 150px; font-size: xx-large" height="150px">
      Anchor Certain（主播端）
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
            </el-icon>
            <p>工作大厅</p>
          </el-menu-item>
          <el-menu-item index="2">
            <el-icon>
              <Bell/>
            </el-icon> <!--Grid has defined in element-plus-->
            <p>申请签约</p>
          </el-menu-item>
          <el-menu-item index="3">
            <el-icon>
              <UserFilled/>
            </el-icon> <!--UserFilled has defined in element-plus-->
            <p>账户设置</p>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!---------main----------->
      <el-container>
        <el-main>
          <!--------page1---------->
          <div v-if="page === '1'">
            <el-table :data="chairman_info" stripe style="width: 100%">
              <el-table-column label="公会账号" width="160">
                <template #default="scope">
                  <p> {{ scope.row.chairman_account }} </p>
                </template>
              </el-table-column>
              <el-table-column label="公会昵称" width="160">
                <template #default="scope">
                  <p> {{ scope.row.chairman_nickname }} </p>
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
                  <el-progress :percentage="parseFloat(scope.row.working_time_percent)"/>
                </template>
              </el-table-column>
              <el-table-column label="可执行操作" width="160">
                <template #default="scope">
                  <el-button @click="handleLiving(scope.row.chairman_account, scope.$index)"
                             v-if="!scope.row.working_status">开播
                  </el-button>
                  <el-button type="danger" @click="handleEndLiving(scope.row.chairman_account, scope.$index)"
                             v-if="scope.row.working_status">停播
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <!--------page2---------->
          <div v-if="page === '2'">
            <div v-for="(waited_chairman, index) in waited_info" style="margin-bottom: 40px" :key="index">
              <el-descriptions
                  border
                  :column="3"
                  style="margin-bottom: 10px"
              >
                <el-descriptions-item label="账号" width="150">{{ waited_chairman.account }}</el-descriptions-item>
                <el-descriptions-item label="公会名" width="200">{{ waited_chairman.nickname }}</el-descriptions-item>
                <el-descriptions-item label="联系方式" width="250">{{
                    waited_chairman.telephone_number === null ? "该公会尚未设置联系方式！" : waited_chairman.telephone_number
                  }}
                </el-descriptions-item>
                <el-descriptions-item label="公会简介" :span="3">
                  {{ waited_chairman.introduction === null ? "该公会尚未设置简介！" : waited_chairman.introduction }}
                </el-descriptions-item>
              </el-descriptions>
              <div style="margin-bottom: 10px">
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-input
                        placeholder="请输入期望薪资"
                        oninput="value=value.replace(/[^\d.]/g,'')"
                        v-model="wanted_salary_time[index].salary"
                    ></el-input>
                  </el-col>
                  <el-col :span="8">
                    <el-input placeholder="请输入预期薪资浮动"
                              oninput="value=value.replace(/[^\d.]/g,'')"
                              v-model="wanted_salary_time[index].salary_fluctuation"
                    ></el-input>
                  </el-col>
                </el-row>
              </div>
              <div style="margin-bottom: 10px">
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-input
                        placeholder="请输入期望直播时长"
                        oninput="value=value.replace(/[^\d.]/g,'')"
                        v-model="wanted_salary_time[index].time"
                    ></el-input>
                  </el-col>
                  <el-col :span="8">
                    <el-input placeholder="请输入预期时长浮动"
                              oninput="value=value.replace(/[^\d.]/g,'')"
                              v-model="wanted_salary_time[index].time_fluctuation"
                    ></el-input>
                  </el-col>
                </el-row>
              </div>
              <el-button @click="wanted(index)">应聘</el-button>
            </div>
          </div>
          <!--------page3---------->
          <div v-if="page === '3'">
            <span style="font-size: xx-large; margin-bottom: 20px; color: #909399">{{ account }}</span>
            <el-table :data="user_info" style="width: 100%">
              <el-table-column label="设置项" width="180" prop="name"></el-table-column>
              <el-table-column label="内容" width="400">
                <template #default="scope">
                  <span v-if="!is_edit[scope.$index]">{{ scope.row.attributes }}</span>
                  <el-input v-if="is_edit[scope.$index] && scope.$index !== 1 && scope.$index !== 2"
                            v-model="scope.row.attributes"
                            oninput="value=value.replace(/\s*/g,'')"
                            placeholder="请输入内容"></el-input>
                  <el-input v-if="is_edit[scope.$index] && scope.$index === 2" v-model="scope.row.attributes"
                            oninput="value=value.replace(/[^\d.]/g,'')"
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
import Cookies from "js-cookie";
import {router} from "@/plugins/router";
import {ElMessage} from "element-plus";
import {attr_name, attr_name_cn} from "@/plugins/utils";

export default {
  name: "anchor_interface",
  data() {
    return {
      loading: true,
      page: '1',
      account: '',
      is_edit: [false, false, false, false],
      user_info: [
        {name: '昵称', attributes: ''},
        {name: '性别', attributes: ''},
        {name: '电话号码', attributes: ''},
        {name: '简介', attributes: ''},
      ],
      chairman_info: [
        {
          chairman_account: '',
          chairman_nickname: '',
          working_status: '',
          working_time_percent: '0'
        }
      ],
      waited_info: [
        {
          account: '',
          nickname: '',
          telephone_number: '',
          introduction: ''
        }
      ],
      wanted_salary_time: [
        {
          salary: '',
          salary_fluctuation: '',
          time: '',
          time_fluctuation: ''
        },
        {
          salary: '',
          salary_fluctuation: '',
          time: '',
          time_fluctuation: ''
        }
      ]
    }
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
    this.getChairmanInfo()
    this.getRandomChairman()
    this.loading = false
  },

  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.account = to.params.account
    })
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

      params.append('type', 'anchor')
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
    async handleLiving(chairman_account, index) {
      for (let i = 0; i < this.chairman_info.length; i++) {
        if (this.chairman_info[i].working_status) {
          ElMessage.error("你已经在" + this.chairman_info[i].chairman_nickname + "公会开播")
          return
        }
      }

      this.loading = true

      let param = new URLSearchParams()

      param.append('anchor_account', this.account)
      param.append('chairman_account', chairman_account)

      await httpGet.get('/token')

      await httpPost.post('/living', param)
          .then(() => {
            this.chairman_info[index].working_status = true
          })

      this.loading = false
    },
    async handleEndLiving(chairman_account) {
      this.loading = true

      let param = new URLSearchParams()

      param.append('anchor_account', this.account)
      param.append('chairman_account', chairman_account)

      await httpGet.get('/token')

      await httpPost.post('endLiving', param)
          .then(() => {
            this.getChairmanInfo()
          })
    },
    async getChairmanInfo() {
      let params = new URLSearchParams()

      params.append('account', this.account)

      await httpGet.get('/token')

      await httpPost.post('/getEmployer', params)
          .then(res => {
            this.chairman_info = res.data
          })
          .catch(err => {
            console.log(err)
          })
    },
    async getUserInfo() {
      await httpGet.get('/getUserInfo?type=anchor&account=' + this.account)
          .then(res => {
            this.user_info = res.data
          })
          .catch(err => {
            console.log(err)
          })
    },
    async getRandomChairman() {
      await httpGet.get('getRandomChairman?account=' + this.account)
          .then((res) => {
            this.waited_info = res.data
          })
    },
    async wanted(index) {
      await httpGet.get('token')

      let param = new URLSearchParams()
      let is_success = false

      param.append('anchor_account', this.account)
      param.append('chairman_account', this.waited_info[index].account)
      param.append('wanted_salary', this.wanted_salary_time[index].salary)
      param.append('wanted_salary_fluctuation', this.wanted_salary_time[index].salary_fluctuation)
      param.append('wanted_goal_time', this.wanted_salary_time[index].time)
      param.append('wanted_goal_time_fluctuation', this.wanted_salary_time[index].time_fluctuation)

      await httpPost.post('wanting', param)
          .then(() => {
            is_success = true
          })

      if (is_success) {
        await this.getRandomChairman()

        this.wanted_salary_time = [
          {
            salary: '',
            salary_fluctuation: '',
            time: '',
            time_fluctuation: ''
          },
          {
            salary: '',
            salary_fluctuation: '',
            time: '',
            time_fluctuation: ''
          }
        ]
      }
    }
  }
}
</script>

<style scoped>

</style>