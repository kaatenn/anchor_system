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
            <el-radio-group v-model="form.type">
              <el-radio label="chairman" size="large" border>公会</el-radio>
              <el-radio label="anchor" size="large" border>主播</el-radio>
            </el-radio-group>
          </div>
        </el-form-item>
        <el-form-item prop="account">
          <el-input
              v-model="form.account"
              placeholder="请输入账号"
              clearable
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
              v-model="form.password"
              placeholder="请输入密码"
              clearable
              show-password
          ></el-input>
        </el-form-item>
      </el-form>
      <div class="butt">
        <el-button type="primary" @click.native.prevent="login('form')"
        >登录</el-button
        >
        <el-button class="shou" @click="register">快速注册</el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "loginInterface",

  data() {
    return {
      form: {
        type: "",
        account: "",
        password: ""
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
  }
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