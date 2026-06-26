<template>
  <div class="university-list-page">
    <h1 class="page-title">院校库</h1>
    <p class="page-subtitle">浏览全国高校信息，支持按层次、类型、地区筛选</p>

    <!-- 筛选栏 -->
    <div class="filter-bar card">
      <el-input v-model="keyword" placeholder="搜索院校名称" clearable style="width: 240px;" @keyup.enter="loadData" />
      <el-select v-model="level" placeholder="院校层次" clearable @change="loadData">
        <el-option label="985" value="985" />
        <el-option label="211" value="211" />
        <el-option label="双一流" value="双一流" />
        <el-option label="公办本科" value="公办本科" />
        <el-option label="民办本科" value="民办本科" />
      </el-select>
      <el-select v-model="type_" placeholder="院校类型" clearable @change="loadData">
        <el-option label="综合" value="综合" />
        <el-option label="理工" value="理工" />
        <el-option label="师范" value="师范" />
        <el-option label="医药" value="医药" />
        <el-option label="财经" value="财经" />
        <el-option label="政法" value="政法" />
        <el-option label="语言" value="语言" />
      </el-select>
      <el-select v-model="province" placeholder="所在省份" clearable @change="loadData">
        <el-option v-for="p in provinces" :key="p" :label="p" :value="p" />
      </el-select>
      <el-button type="primary" @click="loadData">搜索</el-button>
    </div>

    <!-- 列表 -->
    <div v-loading="loading">
      <div class="uni-grid">
        <div v-for="uni in list" :key="uni.id" class="uni-item card" @click="goDetail(uni.id)">
          <h3>{{ uni.name }}</h3>
          <div class="uni-meta">
            <el-tag size="small" :type="levelTag(uni.level)">{{ uni.level }}</el-tag>
            <span>{{ uni.type }}</span>
            <span>{{ uni.city }}，{{ uni.province }}</span>
            <el-tag v-if="uni.is_public" size="small" type="success">公办</el-tag>
            <el-tag v-else size="small" type="warning">民办</el-tag>
          </div>
          <div class="uni-stats">
            <span v-if="uni.postgraduate_rate">保研率 {{ (uni.postgraduate_rate * 100).toFixed(0) }}%</span>
            <span v-if="uni.employment_rate">就业率 {{ (uni.employment_rate * 100).toFixed(0) }}%</span>
          </div>
          <p v-if="uni.top_majors" class="top-majors">王牌：{{ uni.top_majors }}</p>
        </div>
      </div>

      <el-pagination
        v-if="total > pageSize"
        background
        layout="prev, pager, next"
        :total="total"
        :page-size="pageSize"
        v-model:current-page="page"
        @current-change="loadData"
        style="margin-top: 20px; text-align: center;"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { listUniversities } from '../api'

const router = useRouter()
const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20

const keyword = ref('')
const level = ref('')
const type_ = ref('')
const province = ref('')
const provinces = ['北京', '上海', '江苏', '浙江', '山东', '湖北', '四川', '广东', '陕西', '天津', '重庆', '河南', '安徽', '福建', '黑龙江', '辽宁', '湖南']

async function loadData() {
  loading.value = true
  try {
    const resp = await listUniversities({
      keyword: keyword.value || undefined,
      level: level.value || undefined,
      type: type_.value || undefined,
      province: province.value || undefined,
      page: page.value,
      page_size: pageSize,
    })
    list.value = resp.data.items
    total.value = resp.data.total
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function levelTag(level) {
  if (['985', '211'].includes(level)) return 'danger'
  if (level === '双一流') return 'warning'
  return ''
}

function goDetail(id) {
  router.push(`/university/${id}`)
}

onMounted(loadData)
</script>

<style scoped>
.filter-bar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 20px;
}
.uni-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.uni-item {
  cursor: pointer;
  transition: box-shadow 0.2s;
}
.uni-item:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
.uni-item h3 { font-size: 17px; margin-bottom: 8px; color: #1a1a2e; }
.uni-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 14px; color: #666; }
.uni-stats { font-size: 13px; color: #888; display: flex; gap: 16px; margin-bottom: 4px; }
.top-majors { font-size: 13px; color: #fa8c16; }

@media (max-width: 768px) {
  .uni-grid { grid-template-columns: 1fr; }
}
</style>
