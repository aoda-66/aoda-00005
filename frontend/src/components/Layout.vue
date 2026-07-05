<template>
  <div class="app-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1 class="logo">古籍修复</h1>
        <p class="logo-subtitle">数字管理平台</p>
      </div>
      <nav class="sidebar-nav">
        <router-link 
          v-for="item in menuItems" 
          :key="item.name" 
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-text">{{ item.label }}</span>
        </router-link>
      </nav>
    </aside>
    <main class="main-content">
      <header class="top-header">
        <div class="header-left">
          <span class="header-title">{{ currentTitle }}</span>
        </div>
        <div class="header-right">
          <div class="user-info">
            <el-dropdown trigger="click">
              <span class="user-name">
                <el-icon><User /></el-icon>
                {{ currentUser?.real_name || currentUser?.username || '用户' }}
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <span class="current-time">{{ currentTime }}</span>
        </div>
      </header>
      <div class="content-wrapper">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'

const menuItems = [
  { name: 'Books', path: '/books', label: '藏品管理', icon: '📜' },
  { name: 'Damages', path: '/damages', label: '病害存档', icon: '🔍' },
  { name: 'Procedures', path: '/procedures', label: '工序登记', icon: '✏️' },
  { name: 'Materials', path: '/materials', label: '物料台账', icon: '📦' },
  { name: 'Archives', path: '/archives', label: '归档查询', icon: '📚' },
  { name: 'Users', path: '/users', label: '用户管理', icon: '👥' },
  { name: 'Roles', path: '/roles', label: '角色管理', icon: '🛡️' }
]

const currentTime = ref('')
const currentUser = ref(JSON.parse(localStorage.getItem('user') || 'null'))

const currentTitle = computed(() => {
  const item = menuItems.find(i => i.path === '/' + $route.path.split('/')[1])
  return item ? item.label : '古籍修复数字管理平台'
})

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  currentUser.value = null
  ElMessage.success('退出登录成功')
  setTimeout(() => {
    window.location.href = '/login'
  }, 500)
}

let timer = null

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 220px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 30px 20px;
  border-bottom: 1px solid var(--border-color);
  text-align: center;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: var(--primary-color);
  margin: 0;
  font-family: 'Noto Serif SC', 'Songti SC', serif;
}

.logo-subtitle {
  font-size: 12px;
  color: var(--text-secondary);
  margin: 5px 0 0;
}

.sidebar-nav {
  flex: 1;
  padding: 20px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 14px 24px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: rgba(139, 90, 43, 0.05);
  color: var(--primary-color);
}

.nav-item.active {
  background: rgba(139, 90, 43, 0.1);
  color: var(--primary-color);
  border-left-color: var(--primary-color);
}

.nav-icon {
  font-size: 18px;
  margin-right: 12px;
}

.nav-text {
  font-size: 14px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-header {
  height: 60px;
  background: white;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  color: var(--text-primary);
}

.user-info {
  margin-right: 20px;
}

.user-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-secondary);
  cursor: pointer;
}

.user-name:hover {
  color: var(--primary-color);
}

.current-time {
  font-size: 14px;
  color: var(--text-secondary);
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}
</style>