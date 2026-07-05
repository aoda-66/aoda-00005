<template>
  <div class="page-container">
    <div class="page-header">
      <el-button type="primary" @click="openDialog">新增工序记录</el-button>
      <el-select v-model="filterBookId" placeholder="筛选藏品" clearable class="filter-select">
        <el-option v-for="book in books" :key="book.id" :label="book.book_name" :value="book.id" />
      </el-select>
    </div>
    <el-table :data="filteredProcedures" border class="data-table">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="book_name" label="关联藏品" min-width="150">
        <template #default="scope">
          {{ getBookName(scope.row.book_id) }}
        </template>
      </el-table-column>
      <el-table-column prop="procedure_name" label="工序名称" width="120" />
      <el-table-column prop="procedure_type" label="工序类型" width="100" />
      <el-table-column prop="executor" label="执行人" width="100" />
      <el-table-column prop="start_date" label="开始日期" width="120">
        <template #default="scope">
          {{ formatDate(scope.row.start_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="end_date" label="结束日期" width="120">
        <template #default="scope">
          {{ formatDate(scope.row.end_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="duration" label="时长(天)" width="80" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="notes" label="备注" min-width="150" show-overflow-tooltip />
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="editProcedure(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteProcedure(scope.row)">删除</el-button>
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
        <el-form-item label="工序名称" prop="procedure_name">
          <el-input v-model="form.procedure_name" />
        </el-form-item>
        <el-form-item label="工序类型" prop="procedure_type">
          <el-select v-model="form.procedure_type">
            <el-option label="清洗" value="清洗" />
            <el-option label="修补" value="修补" />
            <el-option label="装订" value="装订" />
            <el-option label="托裱" value="托裱" />
            <el-option label="加固" value="加固" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="执行人" prop="executor">
          <el-input v-model="form.executor" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="form.end_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="时长(天)" prop="duration">
          <el-input-number v-model="form.duration" :min="0" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status">
            <el-option label="未开始" value="未开始" />
            <el-option label="进行中" value="进行中" />
            <el-option label="已完成" value="已完成" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input v-model="form.notes" type="textarea" :rows="3" />
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
import { procedureAPI, bookAPI } from '../api'

const procedures = ref([])
const books = ref([])
const filterBookId = ref(null)
const dialogVisible = ref(false)
const dialogTitle = ref('新增工序记录')
const formRef = ref(null)
const editingId = ref(null)

const form = ref({
  book_id: null,
  procedure_name: '',
  procedure_type: '',
  executor: '',
  start_date: '',
  end_date: '',
  duration: null,
  notes: '',
  status: '进行中'
})

const rules = {
  book_id: [{ required: true, message: '请选择关联藏品', trigger: 'change' }],
  procedure_name: [{ required: true, message: '请输入工序名称', trigger: 'blur' }]
}

const filteredProcedures = computed(() => {
  if (!filterBookId.value) return procedures.value
  return procedures.value.filter(p => p.book_id === filterBookId.value)
})

const getBookName = (bookId) => {
  const book = books.value.find(b => b.id === bookId)
  return book ? book.book_name : '未知'
}

const getStatusType = (status) => {
  const types = { '未开始': 'info', '进行中': 'primary', '已完成': 'success' }
  return types[status] || 'info'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const loadProcedures = async () => {
  try {
    procedures.value = await procedureAPI.getAll()
  } catch (error) {
    ElMessage.error('加载工序记录失败')
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
  dialogTitle.value = '新增工序记录'
  form.value = {
    book_id: null,
    procedure_name: '',
    procedure_type: '',
    executor: '',
    start_date: '',
    end_date: '',
    duration: null,
    notes: '',
    status: '进行中'
  }
  dialogVisible.value = true
}

const editProcedure = (row) => {
  editingId.value = row.id
  dialogTitle.value = '编辑工序记录'
  form.value = { ...row }
  dialogVisible.value = true
}

const deleteProcedure = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该工序记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await procedureAPI.delete(row.id)
    ElMessage.success('删除成功')
    loadProcedures()
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
      await procedureAPI.update(editingId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await procedureAPI.create(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadProcedures()
  } catch (error) {
    if (error.response && error.response.status === 400) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('操作失败')
    }
  }
}

loadProcedures()
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