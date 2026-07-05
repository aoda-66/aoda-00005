<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1 class="logo">古籍修复</h1>
        <p class="logo-subtitle">数字管理平台</p>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="0px" class="login-form">
        <el-form-item prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="用户名" 
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="密码" 
            prefix-icon="Lock"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="captcha_code">
          <div class="captcha-row">
            <el-input 
              v-model="form.captcha_code" 
              placeholder="验证码" 
              size="large"
              class="captcha-input"
              @keyup.enter="handleLogin"
            />
            <div class="captcha-image-container">
              <img :src="captchaImage" alt="验证码" class="captcha-image" @click="refreshCaptcha" />
              <span class="refresh-text" @click="refreshCaptcha">换一张</span>
            </div>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" class="login-btn" @click="handleLogin" :loading="loading">
            登 录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { authAPI } from '../api'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const captchaImage = ref('')
const captchaId = ref('')

const form = reactive({
  username: '',
  password: '',
  captcha_code: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  captcha_code: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

const refreshCaptcha = async () => {
  try {
    const response = await authAPI.getCaptcha()
    captchaId.value = response.captcha_id
    captchaImage.value = 'data:image/png;base64,' + response.image
  } catch (error) {
    ElMessage.error('获取验证码失败')
  }
}

const handleLogin = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    const loginData = {
      username: form.username,
      password: form.password,
      captcha_id: captchaId.value,
      captcha_code: form.captcha_code
    }
    const response = await authAPI.login(loginData)
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))
    ElMessage.success('登录成功')
    router.push('/books')
  } catch (error) {
    loading.value = false
    refreshCaptcha()
    if (error.response && error.response.status === 401) {
      ElMessage.error(error.response.data.detail || '登录失败')
    } else {
      ElMessage.error('登录失败，请稍后重试')
    }
  }
}

onMounted(() => {
  refreshCaptcha()
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 420px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  padding: 40px 30px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  font-size: 28px;
  font-weight: bold;
  color: #8b5a2b;
  margin: 0;
  font-family: 'Noto Serif SC', 'Songti SC', serif;
}

.logo-subtitle {
  font-size: 14px;
  color: #999;
  margin: 8px 0 0;
}

.login-form {
  margin-bottom: 20px;
}

.login-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  background: linear-gradient(135deg, #8b5a2b 0%, #a06a36 100%);
  border: none;
}

.login-btn:hover {
  background: linear-gradient(135deg, #a06a36 0%, #8b5a2b 100%);
}

.captcha-row {
  display: flex;
  gap: 12px;
}

.captcha-input {
  flex: 1;
}

.captcha-image-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.captcha-image {
  width: 120px;
  height: 40px;
  border-radius: 4px;
}

.refresh-text {
  font-size: 12px;
  color: #8b5a2b;
  margin-top: 4px;
}

.refresh-text:hover {
  color: #a06a36;
}
</style>