<template>
  <div class="recommendation-page">
    <div v-if="!result" class="empty-state card">
      <p>暂无推荐结果，请先填写考生信息</p>
      <el-button type="primary" @click="$router.push('/score-input')">去填写</el-button>
    </div>

    <div v-else>
      <!-- 摘要 -->
      <div class="summary-card card">
        <div class="summary-header">
          <h2>推荐方案总览</h2>
          <span class="summary-info">
            {{ result.summary.province }} | 总分 {{ result.summary.student_total_score }} |
            位次 {{ result.summary.student_rank }}
          </span>
        </div>
        <div class="summary-stats">
          <div class="stat tier-rush">
            <span class="stat-num">{{ result.summary.rush_count }}</span>
            <span class="stat-label">冲刺院校</span>
          </div>
          <div class="stat tier-stable">
            <span class="stat-num">{{ result.summary.stable_count }}</span>
            <span class="stat-label">稳妥院校</span>
          </div>
          <div class="stat tier-safe">
            <span class="stat-num">{{ result.summary.safe_count }}</span>
            <span class="stat-label">保底院校</span>
          </div>
        </div>
      </div>

      <!-- 三档标签 -->
      <el-tabs v-model="activeTab" type="border-card">
        <el-tab-pane label="冲刺院校" name="rush">
          <template #label>
            <span class="tier-rush">冲刺 ({{ result.rush.length }})</span>
          </template>
          <UniversityCard
            v-for="uni in result.rush"
            :key="uni.university_id"
            :uni="uni"
            tier="冲刺"
          />
        </el-tab-pane>

        <el-tab-pane label="稳妥院校" name="stable">
          <template #label>
            <span class="tier-stable">稳妥 ({{ result.stable.length }})</span>
          </template>
          <UniversityCard
            v-for="uni in result.stable"
            :key="uni.university_id"
            :uni="uni"
            tier="稳妥"
          />
        </el-tab-pane>

        <el-tab-pane label="保底院校" name="safe">
          <template #label>
            <span class="tier-safe">保底 ({{ result.safe.length }})</span>
          </template>
          <UniversityCard
            v-for="uni in result.safe"
            :key="uni.university_id"
            :uni="uni"
            tier="保底"
          />
        </el-tab-pane>
      </el-tabs>

      <!-- 操作 -->
      <div class="actions card">
        <el-button @click="$router.push('/score-input')">重新填写</el-button>
        <el-button type="primary" @click="$router.push('/volunteer-plan')">生成志愿方案</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useScoreStore } from '../stores/score'
import UniversityCard from '../components/UniversityCard.vue'

const scoreStore = useScoreStore()
const result = computed(() => scoreStore.recommendResult)
const activeTab = ref('stable')
</script>

<style scoped>
.summary-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.summary-header h2 { font-size: 22px; color: #1a1a2e; }
.summary-info { color: #888; font-size: 14px; }
.summary-stats {
  display: flex;
  gap: 40px;
}
.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stat-num { font-size: 32px; font-weight: 700; }
.stat-label { font-size: 14px; }
.actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 24px;
}
.empty-state {
  text-align: center;
  padding: 60px;
}
.empty-state p { color: #999; margin-bottom: 16px; }
</style>
