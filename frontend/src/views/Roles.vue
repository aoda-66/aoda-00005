<template>
  <div class="page-container">
    <div class="page-header">
      <el-button type="primary" @click="openDialog">新增角色</el-button>
    </div>
    <el-table :data="roles" border class="data-table">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="角色名称" width="150" />
      <el-table-column prop="code" label="角色编码" width="120" />
      <el-table-column prop="description" label="描述" min-width="200" />
      <el-table-column label="类型" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.is_admin ? 'danger' : 'primary'">
            {{ scope.row.is_admin ? '超级管理员' : '普通角色' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="权限数" width="100">
        <template #default="scope">
          {{ scope.row.permissions.length }}
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button 
            size="small" 
            @click="editRole(scope.row)" 
            :disabled="scope.row.is_admin"
          >编辑</el-button>
          <el-button 
            size="small" 
            type="danger" 
            @click="deleteRole(scope.row)" 
            :disabled="scope.row.is_admin"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="角色编码" prop="code">
          <el-input v-model="form.code" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="权限列表">
          <el-checkbox-group v-model="form.permission_ids">
            <el-checkbox 
              v-for="perm in permissions" 
              :key="perm.id" 
              :label="perm.id"
            >
              {{ perm.name }} ({{ perm.code }})
            </el-checkbox>
          </el-checkbox-group>
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
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { roleAPI } from '../api'

const roles = ref([])
const permissions = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新增角色')
const formRef = ref(null)
const editingId = ref(null)

const form = ref({
  name: '',
  code: '',
  description: '',
  permission_ids: []
})

const rules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入角色编码', trigger: 'blur' }]
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const loadRoles = async () => {
  try {
    roles.value = await roleAPI.getAll()
  } catch (error) {
    ElMessage.error('加载角色失败')
  }
}

const loadPermissions = async () => {
  try {
    permissions.value = await roleAPI.getPermissions()
  } catch (error) {
    ElMessage.error('加载权限失败')
  }
}

const openDialog = () => {
  editingId.value = null
  dialogTitle.value = '新增角色'
  form.value = {
    name: '',
    code: '',
    description: '',
    permission_ids: []
  }
  dialogVisible.value = true
}

const editRole = (row) => {
  editingId.value = row.id
  dialogTitle.value = '编辑角色'
  form.value = {
    name: row.name,
    code: row.code,
    description: row.description,
    permission_ids: row.permissions.map(p => p.id)
  }
  dialogVisible.value = true
}

const deleteRole = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该角色吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await roleAPI.delete(row.id)
    ElMessage.success('删除成功')
    loadRoles()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

const submitForm = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await roleAPI.update(editingId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await roleAPI.create(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadRoles()
  } catch (error) {
    if (error.response && error.response.status === 400) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('操作失败')
    }
  }
}

loadRoles()
loadPermissions()
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

.data-table {
  background: white;
}
</style>