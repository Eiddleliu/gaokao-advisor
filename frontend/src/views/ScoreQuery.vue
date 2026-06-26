<template>
  <div class="score-query-page">
    <h1 class="page-title">分数查询工具</h1>
    <p class="page-subtitle">一分一段表查询、批次分数线、等位分换算</p>

    <el-tabs v-model="activeTab" type="border-card">
      <!-- 一分一段表 -->
      <el-tab-pane label="一分一段表" name="segment">
        <div class="query-bar">
          <el-select v-model="segQuery.province" placeholder="省份">
            <el-option label="山东" value="山东" />
          </el-select>
          <el-select v-model="segQuery.year" placeholder="年份">
            <el-option label="2025" :value="2025" />
          </el-select>
          <el-input-number v-model="segQuery.score_min" :min="300" :max="750" placeholder="最低分" />
          <el-input-number v-model="segQuery.score_max" :min="300" :max="750" placeholder="最高分" />
          <el-button type="primary" @click="querySegments" :loading="segLoading">查询</el-button>
        </div>
        <el-table v-if="segments.length" :data="segments" stripe max-height="500" style="margin-top: 16px;">
          <el-table-column prop="score" label="分数" width="100" />
          <el-table-column prop="count" label="本分人数" width="120" />
          <el-table-column prop="cumulative_count" label="累计人数（位次）" width="160">
            <template #default="{ row }">{{ row.cumulative_count?.toLocaleString() }}</template>
          </el-table-column>
          <el-table-column prop="exam_type" label="科类" width="100" />
        </el-table>
      </el-tab-pane>

      <!-- 批次线 -->
      <el-tab-pane label="批次分数线" name="batch">
        <div class="query-bar">
          <el-select v-model="batchQuery.province" placeholder="省份">
            <el-option label="山东" value="山东" />
          </el-select>
          <el-select v-model="batchQuery.year" placeholder="年份">
            <el-option label="2025" :value="2025" />
          </el-select>
          <el-button type="primary" @click="queryBatchLines" :loading="batchLoading">查询</el-button>
        </div>
        <el-table v-if="batchLines.length" :data="batchLines" stripe style="margin-top: 16px;">
          <el-table-column prop="batch" label="批次" width="200" />
          <el-table-column prop="score" label="分数线" width="150" />
          <el-table-column prop="exam_type" label="科类" width="150" />
        </el-table>
      </el-tab-pane>

      <!-- 等位分 -->
      <el-tab-pane label="等位分换算" name="equiv">
        <div class="query-bar">
          <el-select v-model="equivQuery.province" placeholder="省份">
            <el-option label="山东" value="山东" />
          </el-select>
          <el-select v-model="equivQuery.year" placeholder="年份">
            <el-option label="2025" :value="2025" />
          </el-select>
          <el-input-number v-model="equivQuery.rank" :min="1" :max="1000000" :step="100" placeholder="输入位次" />
          <el-button type="primary" @click="queryEquiv" :loading="equivLoading">换算</el-button>
        </div>
        <div v-if="equivResult" class="equiv-result card">
          <p>位次 <strong>{{ equivResult.rank?.toLocaleString() }}</strong> 对应的等位分为：</p>
          <div class="equiv-score">{{ equivResult.equivalent_score }}</div>
          <p class="equiv-note">实际累计人数：{{ equivResult.actual_cumulative?.toLocaleString() }}</p>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { getScoreSegments, getBatchLines, getEquivalentScore } from '../api'

const activeTab = ref('segment')
const segLoading = ref(false)
const batchLoading = ref(false)
const equivLoading = ref(false)

const segQuery = reactive({ province: '山东', year: 2025, score_min: 550, score_max: 700 })
const batchQuery = reactive({ province: '山东', year: 2025 })
const equivQuery = reactive({ province: '山东', year: 2025, rank: 25000 })

const segments = ref([])
const batchLines = ref([])
const equivResult = ref(null)

async function querySegments() {
  segLoading.value = true
  try {
    const resp = await getScoreSegments(segQuery)
    segments.value = resp.data
  } finally { segLoading.value = false }
}

async function queryBatchLines() {
  batchLoading.value = true
  try {
    const resp = await getBatchLines(batchQuery)
    batchLines.value = resp.data
  } finally { batchLoading.value = false }
}

async function queryEquiv() {
  equivLoading.value = true
  try {
    const resp = await getEquivalentScore(equivQuery)
    equivResult.value = resp.data
  } finally { equivLoading.value = false }
}
</script>

<style scoped>
.query-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
  padding: 16px 0;
}
.equiv-result {
  text-align: center;
  margin-top: 20px;
}
.equiv-score {
  font-size: 64px;
  font-weight: 800;
  color: #1890ff;
  margin: 16px 0;
}
.equiv-note {
  color: #888;
  font-size: 14px;
}
</style>
