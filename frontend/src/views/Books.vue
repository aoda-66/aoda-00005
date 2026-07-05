<template>
  <div class="page-container">
    <div class="page-header">
      <el-button type="primary" @click="openDialog">新增藏品</el-button>
      <el-input 
        v-model="searchKeyword" 
        placeholder="搜索藏品名称或编号" 
        class="search-input"
        clearable
        @input="handleSearch"
      />
    </div>
    <el-table :data="filteredBooks" border class="data-table">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="book_name" label="藏品名称" min-width="150" />
      <el-table-column prop="book_code" label="藏品编号" width="120" />
      <el-table-column prop="author" label="作者" width="100" />
      <el-table-column prop="dynasty" label="朝代" width="80" />
      <el-table-column prop="volume_count" label="卷数" width="60" />
      <el-table-column prop="page_count" label="页数" width="60" />
      <el-table-column prop="current_status" label="当前状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.current_status)">
            {{ scope.row.current_status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="storage_location" label="存放位置" width="120" />
      <el-table-column prop="created_at" label="创建时间" width="160">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="editBook(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteBook(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="藏品名称" prop="book_name">
          <el-input v-model="form.book_name" />
        </el-form-item>
        <el-form-item label="藏品编号" prop="book_code">
          <el-input v-model="form.book_code" />
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="form.author" />
        </el-form-item>
        <el-form-item label="朝代" prop="dynasty">
          <el-input v-model="form.dynasty" />
        </el-form-item>
        <el-form-item label="卷数" prop="volume_count">
          <el-input-number v-model="form.volume_count" :min="0" />
        </el-form-item>
        <el-form-item label="页数" prop="page_count">
          <el-input-number v-model="form.page_count" :min="0" />
        </el-form-item>
        <el-form-item label="存放位置" prop="storage_location">
          <el-input v-model="form.storage_location" />
        </el-form-item>
        <el-form-item label="当前状态" prop="current_status">
          <el-select v-model="form.current_status">
            <el-option label="待修复" value="待修复" />
            <el-option label="修复中" value="修复中" />
            <el-option label="已完成" value="已完成" />
            <el-option label="已归档" value="已归档" />
          </el-select>
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
import { bookAPI } from '../api'

const books = ref([])
const searchKeyword = ref('')
const dialogVisible = ref(false)
const dialogTitle = ref('新增藏品')
const formRef = ref(null)
const editingId = ref(null)

const form = ref({
  book_name: '',
  book_code: '',
  author: '',
  dynasty: '',
  volume_count: null,
  page_count: null,
  storage_location: '',
  current_status: '待修复',
  description: ''
})

const rules = {
  book_name: [{ required: true, message: '请输入藏品名称', trigger: 'blur' }],
  book_code: [{ required: true, message: '请输入藏品编号', trigger: 'blur' }]
}

const filteredBooks = computed(() => {
  if (!searchKeyword.value) return books.value
  const keyword = searchKeyword.value.toLowerCase()
  return books.value.filter(book => 
    book.book_name.toLowerCase().includes(keyword) ||
    book.book_code.toLowerCase().includes(keyword)
  )
})

const getStatusType = (status) => {
  const types = {
    '待修复': 'warning',
    '修复中': 'primary',
    '已完成': 'success',
    '已归档': 'info'
  }
  return types[status] || 'info'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const loadBooks = async () => {
  try {
    books.value = await bookAPI.getAll()
  } catch (error) {
    ElMessage.error('加载藏品失败')
  }
}

const handleSearch = () => {}

const openDialog = () => {
  editingId.value = null
  dialogTitle.value = '新增藏品'
  form.value = {
    book_name: '',
    book_code: '',
    author: '',
    dynasty: '',
    volume_count: null,
    page_count: null,
    storage_location: '',
    current_status: '待修复',
    description: ''
  }
  dialogVisible.value = true
}

const editBook = (row) => {
  editingId.value = row.id
  dialogTitle.value = '编辑藏品'
  form.value = { ...row }
  dialogVisible.value = true
}

const deleteBook = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该藏品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await bookAPI.delete(row.id)
    ElMessage.success('删除成功')
    loadBooks()
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
      await bookAPI.update(editingId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await bookAPI.create(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadBooks()
  } catch (error) {
    if (error.response && error.response.status === 400) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('操作失败')
    }
  }
}

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

.search-input {
  width: 280px;
}

.data-table {
  background: white;
}
</style>