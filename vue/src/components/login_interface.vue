<!-- login interface -->
<template>
  <div class="loginContainer">
    <div class="loginHeader">
      <h2>工会管理系统</h2>
    </div>
    <div class="loginMain">
      <el-form ref="form" :model="form" :rules="rules">
        <el-form-item prop="type">
          <div>
            <el-radio-group v-model="form.type" :disabled="register">
              <el-radio border label="anchor" size="large">主播</el-radio>
              <el-radio border label="chairman" size="large">公会</el-radio>
            </el-radio-group>
          </div>
        </el-form-item>
        <el-form-item prop="account">
          <el-input
              v-model="form.account"
              :disabled="register"
              clearable
              oninput="value=value.replace(/\s*/g,'')"
              placeholder="请输入账号"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
              v-model="form.password"
              :disabled="register"
              clearable
              oninput="value=value.replace(/\s*/g,'')"
              placeholder="请输入密码"
              show-password
          ></el-input>
        </el-form-item>
        <el-form-item v-if="register" prop="sex">
          <el-radio-group v-model="form.sex">
            <el-radio :label="0">男</el-radio>
            <el-radio :label="1">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="register" prop="nickName">
          <el-input
              v-model="form.nickName"
              clearable
              oninput="value=value.replace(/\s*/g,'')"
              placeholder="填写个昵称吧"
          ></el-input>
        </el-form-item>
      </el-form>
      <div class="butt">
        <el-button :disabled="register" type="primary" @click="loginHandler"
        >登录
        </el-button
        >
        <el-button @click="registerHandler">快速注册</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import {ElMessage} from "element-plus";
import {httpGet, httpPost} from "@/plugins/axios";
import Cookies from 'js-cookie';
import {router} from "@/plugins/router";

const MALE = 0
const FEMALE = 1

export default {
  name: "loginInterface",

  data() {
    return {
      register: false,
      form: {
        type: "anchor",
        account: "",
        password: "",
        sex: MALE,
        nickName: "",
      },
      rules: {
        account: [
          {required: true, message: "请输入用户名", trigger: "blur"},
          {min: 3, max: 10, message: "应在 3~10 个字符之间", trigger: "blur"},
        ],
        password: [
          {required: true, message: "请输入密码", trigger: "blur"},
          {min: 6, max: 18, message: "应在 6~18 个字符之间", trigger: "blur"},
        ],
      },
    }
  },

  methods: {
    async loginHandler() {
      let form = this.form

      if (form.account.length < 3 || form.account.length > 10 || form.password.length < 6 || form.password.length > 18) {
        ElMessage.error('请输入正确的账号密码')
        return
      }

      let params = new URLSearchParams();

      params.append('type', form.type)
      params.append('account', form.account)
      params.append('password', form.password)


      // used for access the csrf
      await httpGet.get('/token')

      await httpPost.post('/login', params)
          .then(() => {
            Cookies.set('type', form.type, {expires: 30})
            Cookies.set('account', form.account, {expires: 30})
            let url = form.type + '_interface'
            router.push({name: url, params: {account: form.account}})
          })
          .catch((err) => {
            console.log(err)
            if (err.response.status === 400) {
              ElMessage.error('账号或密码错误！')
              this.form.password = ''
            } else {
              ElMessage.error('请求错误！')
            }
          })
    },

    async registerHandler() {
      let form = this.form

      if (!this.register) {

        // check if the account is existing
        if (form.account.length < 3 || form.account.length > 10 || form.password.length < 6 || form.password.length > 18) {
          ElMessage.error('输入错误！')
          return
        }

        let params = new URLSearchParams()

        params.append('type', form.type)
        params.append('account', form.account)
        params.append('password', form.password)

        await httpGet.get('/token')
        await httpPost.post('/register', params)
            .then(() => {
              Cookies.set('type', form.type, {expires: 30})
              Cookies.set('account', form.account, {expires: 30})
              this.register = true
            })
            .catch(err => {
              if (err.response.status === 400)
                ElMessage.error('账号已被注册！')
              else
                ElMessage.error('请求错误！')
            })
      } else {
        let params = new URLSearchParams()

        params.append('type', form.type)
        params.append('account', form.account)
        params.append('sex', form.sex.toString())
        params.append('nickname', form.nickName)

        if (form.nickName.length > 10) {
          ElMessage.error('昵称长度应小于 10')
          return
        }

        await httpGet.get('/token')

        await httpPost.post('/setBaseInfo', params)
            .then(() => {
              this.$emit('login', this.form.type === "anchor" ? 1 : 2)
              this.register = false // prevent the login can't be used when logout
              let url = form.type + '_interface'
              router.push({name: url, params: {account: form.account}})
            })
            .catch(err => {
              console.log(err)
            })
      }
    }
  },
  emits: ['login']
}
</script>

<style scoped>
.loginContainer {
  margin-left: 25%;
  margin-right: 25%;
  margin-top: 5%;
  height: 50%;
  width: 50%;
  text-align: center;
  line-height: 100%;
  padding-top: 100px;
  padding-bottom: 100px;
  border: #CDD0D6 1px solid;
  border-radius: 8px;
}

.loginHeader {
  margin-bottom: 20px;
  line-height: 50px;
  text-align: center;
  color: white;
  text-shadow: 2px 2px 2px #000000;
}

.loginMain {
  height: 300px;
  width: 400px;
  transform: translate(-50%);
  margin-left: 50%;
}
</style>