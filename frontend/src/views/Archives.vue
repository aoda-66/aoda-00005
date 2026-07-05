<template>
  <div class="page-container">
    <div class="page-header">
      <el-button type="primary" @click="openDialog">新增归档记录</el-button>
      <el-select v-model="filterBookId" placeholder="筛选藏品" clearable class="filter-select">
        <el-option v-for="book in books" :key="book.id" :label="book.book_name" :value="book.id" />
      </el-select>
    </div>
    <el-table :data="filteredArchives" border class="data-table">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="book_name" label="关联藏品" min-width="150">
        <template #default="scope">
          {{ getBookName(scope.row.book_id) }}
        </template>
      </el-table-column>
      <el-table-column prop="archive_type" label="归档类型" width="120">
        <template #default="scope">
          <el-tag>{{ scope.row.archive_type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="archive_name" label="归档名称" min-width="150" />
      <el-table-column prop="file_url" label="文件链接" min-width="200">
        <template #default="scope">
          <a v-if="scope.row.file_url" :href="scope.row.file_url" target="_blank" class="file-link">
            查看文件
          </a>
          <span v-else>无</span>
        </template>
      </el-table-column>
      <el-table-column prop="upload_date" label="上传日期" width="120">
        <template #default="scope">
          {{ formatDate(scope.row.upload_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="editArchive(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteArchive(scope.row)">删除</el-button>
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
        <el-form-item label="归档类型" prop="archive_type">
          <el-select v-model="form.archive_type">
            <el-option label="修复前照片" value="修复前照片" />
            <el-option label="修复后照片" value="修复后照片" />
            <el-option label="修复报告" value="修复报告" />
            <el-option label="病害记录" value="病害记录" />
            <el-option label="工序记录" value="工序记录" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="归档名称" prop="archive_name">
          <el-input v-model="form.archive_name" />
        </el-form-item>
        <el-form-item label="文件路径" prop="file_path">
          <el-input v-model="form.file_path" />
        </el-form-item>
        <el-form-item label="文件链接" prop="file_url">
          <el-input v-model="form.file_url" placeholder="可访问的文件URL" />
        </el-form-item>
        <el-form-item label="上传日期" prop="upload_date">
          <el-date-picker v-model="form.upload_date" type="date" value-format="YYYY-MM-DD" />
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
import { archiveAPI, bookAPI } from '../api'

const archives = ref([])
const books = ref([])
const filterBookId = ref(null)
const dialogVisible = ref(false)
const dialogTitle = ref('新增归档记录')
const formRef = ref(null)
const editingId = ref(null)

const form = ref({
  book_id: null,
  archive_type: '',
  archive_name: '',
  file_path: '',
  file_url: '',
  upload_date: '',
  description: ''
})

const rules = {
  book_id: [{ required: true, message: '请选择关联藏品', trigger: 'change' }],
  archive_type: [{ required: true, message: '请选择归档类型', trigger: 'change' }],
  archive_name: [{ required: true, message: '请输入归档名称', trigger: 'blur' }]
}

const filteredArchives = computed(() => {
  if (!filterBookId.value) return archives.value
  return archives.value.filter(a => a.book_id === filterBookId.value)
})

const getBookName = (bookId) => {
  const book = books.value.find(b => b.id === bookId)
  return book ? book.book_name : '未知'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const loadArchives = async () => {
  try {
    archives.value = await archiveAPI.getAll()
  } catch (error) {
    ElMessage.error('加载归档记录失败')
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
  dialogTitle.value = '新增归档记录'
  form.value = {
    book_id: null,
    archive_type: '',
    archive_name: '',
    file_path: '',
    file_url: '',
    upload_date: '',
    description: ''
  }
  dialogVisible.value = true
}

const editArchive = (row) => {
  editingId.value = row.id
  dialogTitle.value = '编辑归档记录'
  form.value = { ...row }
  dialogVisible.value = true
}

const deleteArchive = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该归档记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await archiveAPI.delete(row.id)
    ElMessage.success('删除成功')
    loadArchives()
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
      await archiveAPI.update(editingId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await archiveAPI.create(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadArchives()
  } catch (error) {
    if (error.response && error.response.status === 400) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('操作失败')
    }
  }
}

loadArchives()
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

.file-link {
  color: var(--primary-color);
  text-decoration: none;
}

.file-link:hover {
  text-decoration: underline;
}
</style>