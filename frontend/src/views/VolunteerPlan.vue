<template>
  <div class="volunteer-plan-page">
    <h1 class="page-title">志愿规划方案</h1>
    <p class="page-subtitle">从推荐结果中选择院校，组合成你的完整志愿表</p>

    <div v-if="!scoreStore.recommendResult" class="empty-state card">
      <p>请先完成智能推荐，再生成志愿方案</p>
      <el-button type="primary" @click="$router.push('/score-input')">去填写分数</el-button>
    </div>

    <div v-else>
      <!-- 方案策略选择 -->
      <div class="card">
        <h3>选择方案策略</h3>
        <el-radio-group v-model="strategy" size="large" style="margin-top: 12px;">
          <el-radio-button value="balanced">均衡方案</el-radio-button>
          <el-radio-button value="rush_first">冲名校优先</el-radio-button>
          <el-radio-button value="major_fit">专业适配优先</el-radio-button>
          <el-radio-button value="safe_first">稳妥保底优先</el-radio-button>
        </el-radio-group>
        <el-button type="primary" @click="generatePlan" :loading="generating" style="margin-left: 20px;">
          生成志愿表
        </el-button>
      </div>

      <!-- 已选志愿 -->
      <div class="card" v-if="plan.length">
        <h3>志愿表（共 {{ plan.length }} 项）</h3>
        <el-table :data="plan" stripe style="margin-top: 12px;">
          <el-table-column type="index" label="序号" width="70" />
          <el-table-column prop="university_name" label="院校" width="200" />
          <el-table-column prop="major_name" label="专业" width="200" />
          <el-table-column prop="tier" label="梯度" width="100">
            <template #default="{ row }">
              <span :class="'tier-' + (row.tier === '冲刺' ? 'rush' : row.tier === '稳妥' ? 'stable' : 'safe')">
                {{ row.tier }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="服从调剂" width="120">
            <template #default="{ row }">
              <el-switch v-model="row.is_adjust" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ $index }">
              <el-button type="danger" size="small" text @click="plan.splice($index, 1)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 风险检测 -->
      <div class="card" v-if="risks.length">
        <h3>风险检测结果</h3>
        <div v-for="risk in risks" :key="risk.message" style="margin-top: 12px;">
          <el-alert
            :title="risk.message"
            :type="risk.level === 'high' ? 'error' : 'warning'"
            :closable="false"
            show-icon
          />
        </div>
      </div>

      <!-- 保存 -->
      <div class="card actions" v-if="plan.length">
        <el-button type="primary" size="large" @click="savePlan" :loading="saving">保存方案</el-button>
        <el-button size="large" @click="checkRisk" :loading="riskChecking">风险检测</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useScoreStore } from '../stores/score'
import { createVolunteerPlan, checkVolunteerRisk } from '../api'

const scoreStore = useScoreStore()
const strategy = ref('balanced')
const plan = ref([])
const risks = ref([])
const generating = ref(false)
const saving = ref(false)
const riskChecking = ref(false)

function generatePlan() {
  const result = scoreStore.recommendResult
  if (!result) return
  generating.value = true

  const newPlan = []
  let order = 1

  // 根据策略决定比例
  let rushLimit, stableLimit, safeLimit
  if (strategy.value === 'rush_first') {
    rushLimit = 40; stableLimit = 30; safeLimit = 26
  } else if (strategy.value === 'safe_first') {
    rushLimit = 20; stableLimit = 30; safeLimit = 46
  } else if (strategy.value === 'major_fit') {
    rushLimit = 25; stableLimit = 40; safeLimit = 31
  } else {
    rushLimit = 30; stableLimit = 36; safeLimit = 30
  }

  // 冲刺
  for (const uni of result.rush.slice(0, rushLimit)) {
    for (const major of uni.recommended_majors.slice(0, 1)) {
      newPlan.push({
        university_id: uni.university_id,
        university_name: uni.university_name,
        major_id: major.major_id,
        major_name: major.major_name,
        tier: '冲刺',
        order: order++,
        is_adjust: true,
      })
    }
  }

  // 稳妥
  for (const uni of result.stable.slice(0, stableLimit)) {
    for (const major of uni.recommended_majors.slice(0, 1)) {
      newPlan.push({
        university_id: uni.university_id,
        university_name: uni.university_name,
        major_id: major.major_id,
        major_name: major.major_name,
        tier: '稳妥',
        order: order++,
        is_adjust: true,
      })
    }
  }

  // 保底
  for (const uni of result.safe.slice(0, safeLimit)) {
    for (const major of uni.recommended_majors.slice(0, 1)) {
      newPlan.push({
        university_id: uni.university_id,
        university_name: uni.university_name,
        major_id: major.major_id,
        major_name: major.major_name,
        tier: '保底',
        order: order++,
        is_adjust: true,
      })
    }
  }

  plan.value = newPlan
  risks.value = []
  generating.value = false
  ElMessage.success(`已生成 ${newPlan.length} 个志愿选项`)
}

async function checkRisk() {
  riskChecking.value = true
  try {
    const resp = await checkVolunteerRisk(plan.value)
    risks.value = resp.data.risks || []
    if (risks.value.length === 0) {
      ElMessage.success('未检测到明显风险')
    }
  } catch (e) {
    ElMessage.error('风险检测失败')
  } finally {
    riskChecking.value = false
  }
}

async function savePlan() {
  saving.value = true
  try {
    await createVolunteerPlan({
      user_id: 1,
      score_id: 1,
      name: `${strategy.value === 'rush_first' ? '冲名校' : strategy.value === 'major_fit' ? '专业适配' : strategy.value === 'safe_first' ? '稳妥保底' : '均衡'}方案`,
      strategy: strategy.value,
      choices: plan.value,
    })
    ElMessage.success('方案已保存')
  } catch (e) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.actions { display: flex; gap: 12px; justify-content: center; }
.empty-state { text-align: center; padding: 60px; }
.empty-state p { color: #999; margin-bottom: 16px; }
</style>
