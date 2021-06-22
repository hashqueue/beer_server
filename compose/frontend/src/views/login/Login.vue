<template>
  <common-layout>
    <div class="top">
      <div class="header">
        <img alt="logo" class="logo" src="@/assets/img/logo.png" />
        <span class="title">{{ systemName }}</span>
      </div>
      <div class="desc">Ant Design 是西湖区最具影响力的 Web 设计规范</div>
    </div>
    <div class="loginAndRegister">
      <a-tabs
        :activeKey="activeKey"
        size="large"
        :tabBarStyle="{ textAlign: 'center' }"
        style="padding: 0 2px"
        @change="changeActiveKey"
      >
        <a-tab-pane tab="登录" key="1">
          <a-form-model ref="loginRuleFormRef" :model="loginForm" :rules="loginFormRules">
            <a-form-model-item prop="username">
              <a-input allowClear size="large" placeholder="用户名/邮箱" v-model="loginForm.username">
                <a-icon slot="prefix" type="user" />
              </a-input>
            </a-form-model-item>
            <a-form-model-item prop="password">
              <a-input-password
                allowClear
                size="large"
                @pressEnter="submitLoginCallback($event)"
                placeholder="密码"
                v-model="loginForm.password"
                type="password"
              >
                <a-icon slot="prefix" type="lock" />
              </a-input-password>
            </a-form-model-item>
            <a-button
              type="primary"
              style="width: 100%; margin-top: 24px"
              size="large"
              @click="submitLoginForm('loginRuleFormRef')"
              >登录</a-button
            >
            <div style="margin-top: 20px">演示环境禁用了所有账户的`数据删除权限`</div>
            <div style="margin-top: 8px">管理员账号：anonymous密码：python.8000.*</div>
            <div style="margin-top: 8px">普通用户账号：username1密码：username1</div>
          </a-form-model>
        </a-tab-pane>
        <a-tab-pane tab="注册" key="2">
          <a-form-model ref="registerRuleFormRef" :model="registerForm" :rules="registerFormRules">
            <a-form-model-item prop="username">
              <a-input allowClear size="large" placeholder="用户名" v-model="registerForm.username">
                <a-icon slot="prefix" type="user" />
              </a-input>
            </a-form-model-item>
            <a-form-model-item prop="email">
              <a-input allowClear size="large" placeholder="邮箱" v-model="registerForm.email">
                <a-icon slot="prefix" type="mail" />
              </a-input>
            </a-form-model-item>
            <a-form-model-item prop="password">
              <a-input-password
                allowClear
                size="large"
                placeholder="密码"
                v-model="registerForm.password"
                type="password"
              >
                <a-icon slot="prefix" type="lock" />
              </a-input-password>
            </a-form-model-item>
            <a-form-model-item prop="password_confirm">
              <a-input-password
                allowClear
                size="large"
                placeholder="确认密码"
                v-model="registerForm.password_confirm"
                type="password"
              >
                <a-icon slot="prefix" type="lock" />
              </a-input-password>
            </a-form-model-item>
            <a-button
              type="primary"
              style="width: 100%; margin-top: 24px"
              size="large"
              @click="submitRegisterForm('registerRuleFormRef')"
              >注册</a-button
            >
          </a-form-model>
        </a-tab-pane>
      </a-tabs>
    </div>
  </common-layout>
</template>

<script>
import CommonLayout from '@/layouts/CommonLayout'
import { getUserProfile, userLogin, userRegister } from '@/services/users'
import { setToken, setUserId } from '@/utils/auth'
import { mapMutations } from 'vuex'
export default {
  name: 'Login',
  components: { CommonLayout },
  data() {
    let validatePasswordConfirm = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    let validateMail = (rule, value, callback) => {
      if (!/\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/g.test(value)) {
        callback(new Error('输入的邮箱格式不对'))
      } else {
        callback()
      }
    }
    return {
      activeKey: '1',
      loginForm: {
        username: '',
        password: ''
      },
      loginFormRules: {
        username: [{ required: true, message: '请输入用户名/邮箱', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      },
      registerForm: {
        username: '',
        email: '',
        password: '',
        password_confirm: ''
      },
      registerFormRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 6, max: 150, message: '用户名不能小于6个字符或超过150个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { min: 8, max: 254, message: '邮箱不能小于8个字符或超过254个字符', trigger: 'blur' },
          { validator: validateMail, trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 128, message: '密码不能小于6个字符或超过128个字符', trigger: 'blur' }
        ],
        password_confirm: [
          { required: true, message: '请输入确认密码', trigger: 'blur' },
          { min: 6, max: 128, message: '密码不能小于6个字符或超过128个字符', trigger: 'blur' },
          { validator: validatePasswordConfirm, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    systemName() {
      return this.$store.state.setting.systemName
    }
  },
  methods: {
    ...mapMutations('account', ['setUser']),
    // eslint-disable-next-line no-unused-vars
    submitLoginCallback(e) {
      this.submitLoginForm('loginRuleFormRef')
    },
    changeActiveKey(key) {
      if (key === '2') {
        this.activeKey = '2'
      } else {
        this.activeKey = '1'
      }
    },
    submitLoginForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          userLogin(this.loginForm)
            .then((res) => {
              this.resetForm('loginRuleFormRef')
              setToken(res.data.access)
              setUserId(res.data.user_id)
              // 获取当前登录用户的信息
              getUserProfile(res.data.user_id).then((res) => {
                this.setUser(res.data)
              })
              this.$message.success(res.message)
              this.$router.push('/dashboard/workplace')
            })
            .catch((err) => {
              console.log(err)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    submitRegisterForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          userRegister(this.registerForm).then((res) => {
            this.loginForm.username = this.registerForm.username
            this.loginForm.password = this.registerForm.password
            this.resetForm('registerRuleFormRef')
            this.$message.success(res.message)
            this.activeKey = '1'
          })
          // console.log('registerSubmit')
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 重置表单数据
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style lang="less" scoped>
.common-layout {
  .top {
    text-align: center;
    .header {
      height: 44px;
      line-height: 44px;
      a {
        text-decoration: none;
      }
      .logo {
        height: 44px;
        vertical-align: top;
        margin-right: 16px;
      }
      .title {
        font-size: 33px;
        color: @title-color;
        font-family: 'Myriad Pro', 'Helvetica Neue', Arial, Helvetica, sans-serif;
        font-weight: 600;
        position: relative;
        top: 2px;
      }
    }
    .desc {
      font-size: 14px;
      color: @text-color-second;
      margin-top: 12px;
      margin-bottom: 40px;
    }
  }
  .loginAndRegister {
    width: 368px;
    margin: 0 auto;
    @media screen and (max-width: 576px) {
      width: 95%;
    }
    @media screen and (max-width: 320px) {
      .captcha-button {
        font-size: 14px;
      }
    }
    .icon {
      font-size: 24px;
      color: @text-color-second;
      margin-left: 16px;
      vertical-align: middle;
      cursor: pointer;
      transition: color 0.3s;
      &:hover {
        color: @primary-color;
      }
    }
  }
}
</style>
