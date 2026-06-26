<template>
  <div class="university-detail-page" v-loading="loading">
    <div v-if="uni" class="card">
      <el-page-header @back="$router.back()" :title="'返回'" />

      <h1 class="page-title" style="margin-top: 16px;">{{ uni.name }}</h1>
      <div class="uni-header-info">
        <el-tag :type="levelTag(uni.level)">{{ uni.level }}</el-tag>
        <el-tag>{{ uni.type }}</el-tag>
        <el-tag :type="uni.is_public ? 'success' : 'warning'">{{ uni.is_public ? '公办' : '民办' }}</el-tag>
        <span>{{ uni.city }}，{{ uni.province }}</span>
      </div>

      <el-descriptions :column="3" border style="margin-top: 20px;">
        <el-descriptions-item label="学费范围">
          {{ uni.tuition_min ? `${uni.tuition_min} - ${uni.tuition_max} 元/年` : '未知' }}
        </el-descriptions-item>
        <el-descriptions-item label="保研率">
          {{ uni.postgraduate_rate ? `${(uni.postgraduate_rate * 100).toFixed(1)}%` : '未知' }}
        </el-descriptions-item>
        <el-descriptions-item label="就业率">
          {{ uni.employment_rate ? `${(uni.employment_rate * 100).toFixed(1)}%` : '未知' }}
        </el-descriptions-item>
        <el-descriptions-item label="平均薪资">
          {{ uni.avg_salary ? `${uni.avg_salary} 元/月` : '未知' }}
        </el-descriptions-item>
        <el-descriptions-item label="王牌专业" :span="2">
          {{ uni.top_majors || '未知' }}
        </el-descriptions-item>
      </el-descriptions>

      <p v-if="uni.description" class="uni-desc">{{ uni.description }}</p>
    </div>

    <!-- 专业列表 -->
    <div class="card" v-if="majors.length">
      <h2>开设专业</h2>
      <el-table :data="majors" stripe style="width: 100%; margin-top: 12px;">
        <el-table-column prop="name" label="专业名称" width="180" />
        <el-table-column prop="category" label="专业大类" width="120" />
        <el-table-column prop="duration" label="学制" width="80" />
        <el-table-column prop="degree" label="学位" width="100" />
        <el-table-column label="选科要求" width="150">
          <template #default="{ row }">{{ row.subject_requirement || '不限' }}</template>
        </el-table-column>
        <el-table-column label="单科权重">
          <template #default="{ row }">
            <span v-if="row.subject_weights">
              {{ Object.entries(row.subject_weights).map(([k, v]) => `${k}${(v*100).toFixed(0)}%`).join(' ') }}
            </span>
            <span v-else class="text-muted">未设置</span>
          </template>
        </el-table-column>
        <el-table-column label="单科最低要求">
          <template #default="{ row }">
            <el-tag v-for="(v, k) in (row.min_subject_scores || {})" :key="k" type="danger" size="small" style="margin-right:4px;">
              {{ k }} >= {{ v }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 录取数据 -->
    <div class="card" v-if="admissions.length">
      <h2>历年录取数据（山东）</h2>
      <el-table :data="admissions" stripe style="width: 100%; margin-top: 12px;">
        <el-table-column prop="year" label="年份" width="80" />
        <el-table-column prop="major_name" label="专业" width="160" />
        <el-table-column prop="major_category" label="大类" width="100" />
        <el-table-column prop="min_total_score" label="最低总分" width="100" />
        <el-table-column prop="avg_total_score" label="平均总分" width="100" />
        <el-table-column prop="min_rank" label="最低位次" width="100">
          <template #default="{ row }">{{ row.min_rank?.toLocaleString() }}</template>
        </el-table-column>
        <el-table-column label="单科平均分" min-width="300">
          <template #default="{ row }">
            <div class="subject-avg-grid">
              <span v-for="(val, subj) in row.subject_avg" :key="subj" v-if="val" class="subject-avg-item">
                {{ subj }}: <strong>{{ val }}</strong>
              </span>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getUniversityDetail, getUniversityMajors, getUniversityAdmissions } from '../api'

const route = useRoute()
const loading = ref(true)
const uni = ref(null)
const majors = ref([])
const admissions = ref([])

function levelTag(level) {
  if (['985', '211'].includes(level)) return 'danger'
  if (level === '双一流') return 'warning'
  return ''
}

onMounted(async () => {
  try {
    const id = route.params.id
    const [uniResp, majorsResp, admResp] = await Promise.all([
      getUniversityDetail(id),
      getUniversityMajors(id),
      getUniversityAdmissions(id, { province: '山东' }).catch(() => ({ data: [] })),
    ])
    uni.value = uniResp.data
    majors.value = majorsResp.data
    admissions.value = admResp.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.uni-header-info { display: flex; align-items: center; gap: 8px; margin-top: 8px; font-size: 15px; color: #666; }
.uni-desc { margin-top: 16px; color: #555; line-height: 1.8; }
h2 { font-size: 18px; margin-bottom: 8px; color: #1a1a2e; }
.subject-avg-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.subject-avg-item { font-size: 13px; color: #555; background: #f5f5f5; padding: 2px 8px; border-radius: 4px; }
.text-muted { color: #ccc; font-size: 13px; }
</style>
