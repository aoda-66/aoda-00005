<template>
  <div class="page-container">
    <div class="page-header">
      <el-button type="primary" @click="openDialog">新增用户</el-button>
      <el-input 
        v-model="searchKeyword" 
        placeholder="搜索用户名或姓名" 
        class="search-input"
        clearable
        @input="handleSearch"
      />
    </div>
    <el-table :data="filteredUsers" border class="data-table">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="real_name" label="姓名" width="100" />
      <el-table-column prop="email" label="邮箱" width="180" />
      <el-table-column prop="phone" label="电话" width="120" />
      <el-table-column label="角色" width="150">
        <template #default="scope">
          <el-tag :type="scope.row.role.is_admin ? 'danger' : 'primary'">
            {{ scope.row.role.name }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.is_active ? 'success' : 'info'">
            {{ scope.row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="editUser(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteUser(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="姓名" prop="real_name">
          <el-input v-model="form.real_name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="角色" prop="role_id">
          <el-select v-model="form.role_id">
            <el-option 
              v-for="role in roles" 
              :key="role.id" 
              :label="role.name" 
              :value="role.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!editingId">
          <el-input v-model="form.password" type="password" placeholder="至少6位" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { userAPI, roleAPI } from '../api'

const users = ref([])
const roles = ref([])
const searchKeyword = ref('')
const dialogVisible = ref(false)
const dialogTitle = ref('新增用户')
const formRef = ref(null)
const editingId = ref(null)

const form = ref({
  username: '',
  real_name: '',
  email: '',
  phone: '',
  role_id: '',
  password: '',
  is_active: true
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  role_id: [{ required: true, message: '请选择角色', trigger: 'change' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur', min: 6 }]
}

const filteredUsers = computed(() => {
  if (!searchKeyword.value) return users.value
  const keyword = searchKeyword.value.toLowerCase()
  return users.value.filter(user => 
    user.username.toLowerCase().includes(keyword) ||
    (user.real_name && user.real_name.toLowerCase().includes(keyword))
  )
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const loadUsers = async () => {
  try {
    users.value = await userAPI.getAll()
  } catch (error) {
    ElMessage.error('加载用户失败')
  }
}

const loadRoles = async () => {
  try {
    roles.value = await roleAPI.getAll()
  } catch (error) {
    ElMessage.error('加载角色失败')
  }
}

const handleSearch = () => {}

const openDialog = () => {
  editingId.value = null
  dialogTitle.value = '新增用户'
  form.value = {
    username: '',
    real_name: '',
    email: '',
    phone: '',
    role_id: '',
    password: '',
    is_active: true
  }
  dialogVisible.value = true
}

const editUser = (row) => {
  editingId.value = row.id
  dialogTitle.value = '编辑用户'
  form.value = {
    username: row.username,
    real_name: row.real_name,
    email: row.email,
    phone: row.phone,
    role_id: row.role_id,
    password: '',
    is_active: row.is_active
  }
  dialogVisible.value = true
}

const deleteUser = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await userAPI.delete(row.id)
    ElMessage.success('删除成功')
    loadUsers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const submitForm = async () => {
  try {
    await formRef.value.validate()
    const submitData = { ...form.value }
    if (!submitData.password) delete submitData.password
    if (editingId.value) {
      await userAPI.update(editingId.value, submitData)
      ElMessage.success('更新成功')
    } else {
      await userAPI.create(submitData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadUsers()
  } catch (error) {
    if (error.response && error.response.status === 400) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('操作失败')
    }
  }
}

loadUsers()
loadRoles()
</script>

<style scoped>
.page-container {
  max-width: 1400px;
}

.page-header {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.search-input {
  width: 280px;
}

.data-table {
  background: white;
}
</style>