<template>
  <div class="page-container">
    <div class="page-header">
      <el-button type="primary" @click="openDialog">新增病害记录</el-button>
      <el-select v-model="filterBookId" placeholder="筛选藏品" clearable class="filter-select">
        <el-option v-for="book in books" :key="book.id" :label="book.book_name" :value="book.id" />
      </el-select>
    </div>
    <el-table :data="filteredDamages" border class="data-table">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="book_name" label="关联藏品" min-width="150">
        <template #default="scope">
          {{ getBookName(scope.row.book_id) }}
        </template>
      </el-table-column>
      <el-table-column prop="damage_type" label="病害类型" width="120" />
      <el-table-column prop="damage_level" label="病害等级" width="100">
        <template #default="scope">
          <el-tag :type="getLevelType(scope.row.damage_level)">
            {{ scope.row.damage_level || '未知' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="location" label="位置" width="120" />
      <el-table-column prop="damage_date" label="发现日期" width="120">
        <template #default="scope">
          {{ formatDate(scope.row.damage_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="160">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="editDamage(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteDamage(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="关联藏品" prop="book_id">
          <el-select v-model="form.book_id" placeholder="请选择藏品">
            <el-option v-for="book in books" :key="book.id" :label="book.book_name" :value="book.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="病害类型" prop="damage_type">
          <el-input v-model="form.damage_type" />
        </el-form-item>
        <el-form-item label="病害等级" prop="damage_level">
          <el-select v-model="form.damage_level">
            <el-option label="轻微" value="轻微" />
            <el-option label="中度" value="中度" />
            <el-option label="严重" value="严重" />
          </el-select>
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="form.location" />
        </el-form-item>
        <el-form-item label="发现日期" prop="damage_date">
          <el-date-picker v-model="form.damage_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
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
import { damageAPI, bookAPI } from '../api'

const damages = ref([])
const books = ref([])
const filterBookId = ref(null)
const dialogVisible = ref(false)
const dialogTitle = ref('新增病害记录')
const formRef = ref(null)
const editingId = ref(null)

const form = ref({
  book_id: null,
  damage_type: '',
  damage_level: '',
  location: '',
  damage_date: '',
  description: ''
})

const rules = {
  book_id: [{ required: true, message: '请选择关联藏品', trigger: 'change' }],
  damage_type: [{ required: true, message: '请输入病害类型', trigger: 'blur' }]
}

const filteredDamages = computed(() => {
  if (!filterBookId.value) return damages.value
  return damages.value.filter(d => d.book_id === filterBookId.value)
})

const getBookName = (bookId) => {
  const book = books.value.find(b => b.id === bookId)
  return book ? book.book_name : '未知'
}

const getLevelType = (level) => {
  const types = { '轻微': 'success', '中度': 'warning', '严重': 'danger' }
  return types[level] || 'info'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const loadDamages = async () => {
  try {
    damages.value = await damageAPI.getAll()
  } catch (error) {
    ElMessage.error('加载病害记录失败')
  }
}

const loadBooks = async () => {
  try {
    books.value = await bookAPI.getAll()
  } catch (error) {
    ElMessage.error('加载藏品列表失败')
  }
}

const openDialog = () => {
  editingId.value = null
  dialogTitle.value = '新增病害记录'
  form.value = {
    book_id: null,
    damage_type: '',
    damage_level: '',
    location: '',
    damage_date: '',
    description: ''
  }
  dialogVisible.value = true
}

const editDamage = (row) => {
  editingId.value = row.id
  dialogTitle.value = '编辑病害记录'
  form.value = { ...row }
  dialogVisible.value = true
}

const deleteDamage = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该病害记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await damageAPI.delete(row.id)
    ElMessage.success('删除成功')
    loadDamages()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const submitForm = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await damageAPI.update(editingId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await damageAPI.create(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadDamages()
  } catch (error) {
    if (error.response && error.response.status === 400) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('操作失败')
    }
  }
}

loadDamages()
loadBooks()
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

.filter-select {
  width: 200px;
}

.data-table {
  background: white;
}
</style>