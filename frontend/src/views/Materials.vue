<template>
  <div class="page-container">
    <div class="page-header">
      <el-button type="primary" @click="openDialog">新增物料</el-button>
      <el-button @click="loadLowStock" class="low-stock-btn">库存预警</el-button>
      <el-input 
        v-model="searchKeyword" 
        placeholder="搜索物料名称或编号" 
        class="search-input"
        clearable
        @input="handleSearch"
      />
    </div>
    <el-table :data="filteredMaterials" border class="data-table">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="material_name" label="物料名称" min-width="150" />
      <el-table-column prop="material_code" label="物料编号" width="120" />
      <el-table-column prop="unit" label="单位" width="80" />
      <el-table-column prop="stock_quantity" label="库存数量" width="100">
        <template #default="scope">
          <span :class="{ 'low-stock': scope.row.stock_quantity <= scope.row.min_stock }">
            {{ scope.row.stock_quantity }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="min_stock" label="最低库存" width="100" />
      <el-table-column prop="price" label="单价" width="100">
        <template #default="scope">
          ¥{{ scope.row.price || 0 }}
        </template>
      </el-table-column>
      <el-table-column prop="supplier" label="供应商" width="120" />
      <el-table-column prop="storage_location" label="存放位置" width="120" />
      <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="editMaterial(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteMaterial(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="物料名称" prop="material_name">
          <el-input v-model="form.material_name" />
        </el-form-item>
        <el-form-item label="物料编号" prop="material_code">
          <el-input v-model="form.material_code" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="form.unit" />
        </el-form-item>
        <el-form-item label="库存数量" prop="stock_quantity">
          <el-input-number v-model="form.stock_quantity" :min="0" step="0.1" />
        </el-form-item>
        <el-form-item label="最低库存" prop="min_stock">
          <el-input-number v-model="form.min_stock" :min="0" step="0.1" />
        </el-form-item>
        <el-form-item label="单价" prop="price">
          <el-input-number v-model="form.price" :min="0" step="0.01" />
        </el-form-item>
        <el-form-item label="供应商" prop="supplier">
          <el-input v-model="form.supplier" />
        </el-form-item>
        <el-form-item label="存放位置" prop="storage_location">
          <el-input v-model="form.storage_location" />
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
import { materialAPI } from '../api'

const materials = ref([])
const searchKeyword = ref('')
const dialogVisible = ref(false)
const dialogTitle = ref('新增物料')
const formRef = ref(null)
const editingId = ref(null)

const form = ref({
  material_name: '',
  material_code: '',
  unit: '',
  stock_quantity: 0,
  min_stock: 0,
  price: null,
  supplier: '',
  storage_location: '',
  description: ''
})

const rules = {
  material_name: [{ required: true, message: '请输入物料名称', trigger: 'blur' }],
  material_code: [{ required: true, message: '请输入物料编号', trigger: 'blur' }]
}

const filteredMaterials = computed(() => {
  if (!searchKeyword.value) return materials.value
  const keyword = searchKeyword.value.toLowerCase()
  return materials.value.filter(m => 
    m.material_name.toLowerCase().includes(keyword) ||
    m.material_code.toLowerCase().includes(keyword)
  )
})

const loadMaterials = async () => {
  try {
    materials.value = await materialAPI.getAll()
  } catch (error) {
    ElMessage.error('加载物料失败')
  }
}

const loadLowStock = async () => {
  try {
    const lowStock = await materialAPI.getLowStock()
    if (lowStock.length === 0) {
      ElMessage.info('暂无库存预警物料')
    } else {
      materials.value = lowStock
      ElMessage.warning(`共 ${lowStock.length} 种物料库存不足`)
    }
  } catch (error) {
    ElMessage.error('查询库存预警失败')
  }
}

const handleSearch = () => {}

const openDialog = () => {
  editingId.value = null
  dialogTitle.value = '新增物料'
  form.value = {
    material_name: '',
    material_code: '',
    unit: '',
    stock_quantity: 0,
    min_stock: 0,
    price: null,
    supplier: '',
    storage_location: '',
    description: ''
  }
  dialogVisible.value = true
}

const editMaterial = (row) => {
  editingId.value = row.id
  dialogTitle.value = '编辑物料'
  form.value = { ...row }
  dialogVisible.value = true
}

const deleteMaterial = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该物料吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await materialAPI.delete(row.id)
    ElMessage.success('删除成功')
    loadMaterials()
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
      await materialAPI.update(editingId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await materialAPI.create(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadMaterials()
  } catch (error) {
    if (error.response && error.response.status === 400) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('操作失败')
    }
  }
}

loadMaterials()
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

.low-stock-btn {
  background: var(--warning-color);
  border-color: var(--warning-color);
  color: white;
}

.low-stock-btn:hover {
  background: #C49A6C;
  border-color: #C49A6C;
}

.data-table {
  background: white;
}

.low-stock {
  color: var(--danger-color);
  font-weight: bold;
}
</style>