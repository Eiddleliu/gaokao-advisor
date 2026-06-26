<template>
  <div class="uni-card" @click="goDetail">
    <div class="card-header">
      <div class="uni-info">
        <h3 class="uni-name">{{ uni.university_name }}</h3>
        <div class="uni-tags">
          <el-tag v-for="tag in uni.tags" :key="tag" size="small" :type="tagType(tag)">{{ tag }}</el-tag>
          <span class="uni-location">{{ uni.city }}，{{ uni.province }}</span>
        </div>
      </div>
      <div class="tier-badge" :class="tierClass">{{ tier }}</div>
    </div>

    <!-- 核心指标 -->
    <div class="metrics">
      <div class="metric">
        <span class="metric-label">位次匹配</span>
        <el-progress :percentage="uni.rank_match_score" :stroke-width="8" :color="progressColor" />
      </div>
      <div class="metric">
        <span class="metric-label">单科适配</span>
        <el-progress :percentage="uni.subject_adapt_score" :stroke-width="8" color="#722ed1" />
      </div>
      <div class="metric">
        <span class="metric-label">综合得分</span>
        <span class="metric-value">{{ uni.total_score.toFixed(1) }}</span>
      </div>
    </div>

    <!-- 3年位次 -->
    <div class="rank-history" v-if="uni.min_rank_3yr.length">
      <span class="label">近三年最低位次：</span>
      <span v-for="(r, i) in uni.min_rank_3yr" :key="i" class="rank-val">{{ r.toLocaleString() }}</span>
    </div>

    <!-- 推荐专业 -->
    <div class="majors-section" v-if="uni.recommended_majors.length">
      <h4>推荐专业</h4>
      <div class="major-item" v-for="major in uni.recommended_majors.slice(0, 3)" :key="major.major_id">
        <div class="major-header">
          <span class="major-name">{{ major.major_name }}</span>
          <span class="major-category tag tag-blue">{{ major.category }}</span>
          <span class="major-score">适配度 {{ major.subject_adapt_score.toFixed(1) }}</span>
        </div>
        <div class="major-tags">
          <el-tag v-for="tag in major.adapt_tags" :key="tag" type="success" size="small">{{ tag }}</el-tag>
          <el-tag v-for="note in major.risk_notes" :key="note" type="danger" size="small">{{ note }}</el-tag>
        </div>
        <!-- 单科对比 -->
        <div class="subject-compare" v-if="major.subject_match_details.length">
          <span v-for="sd in major.subject_match_details" :key="sd.subject" class="subject-item"
            :class="{ 'above': sd.is_above_avg, 'below': !sd.is_above_avg }">
            {{ sd.subject }}: {{ sd.student_score }}
            <template v-if="sd.major_avg_score">
              vs 均{{ sd.major_avg_score }}
            </template>
          </span>
        </div>
      </div>
    </div>

    <!-- 风险标注 -->
    <div class="risk-section" v-if="uni.risk_level !== 'low'">
      <el-alert
        :title="uni.risk_level === 'high' ? '存在多项风险，请仔细核查' : '存在潜在风险，建议关注'"
        :type="uni.risk_level === 'high' ? 'error' : 'warning'"
        :closable="false"
        show-icon
      />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  uni: { type: Object, required: true },
  tier: { type: String, default: '' },
})

const router = useRouter()

const tierClass = props.tier === '冲刺' ? 'rush' : props.tier === '稳妥' ? 'stable' : 'safe'

function tagType(tag) {
  if (['985', '211', '双一流'].includes(tag)) return 'danger'
  if (['公办本科', '公办专科'].includes(tag)) return ''
  return 'info'
}

function progressColor(pct) {
  if (pct >= 80) return '#52c41a'
  if (pct >= 60) return '#faad14'
  return '#f5222d'
}

function goDetail() {
  router.push(`/university/${props.uni.university_id}`)
}
</script>

<style scoped>
.uni-card {
  background: white;
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  cursor: pointer;
  transition: box-shadow 0.2s;
}
.uni-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; }
.uni-name { font-size: 18px; font-weight: 600; color: #1a1a2e; margin-bottom: 6px; }
.uni-tags { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.uni-location { color: #888; font-size: 13px; margin-left: 4px; }
.tier-badge {
  padding: 4px 14px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}
.tier-badge.rush { background: #fff1f0; color: #f5222d; }
.tier-badge.stable { background: #e6f7e9; color: #52c41a; }
.tier-badge.safe { background: #e8f4fd; color: #1890ff; }
.metrics {
  display: flex;
  gap: 24px;
  margin: 16px 0;
  align-items: center;
}
.metric { flex: 1; }
.metric-label { font-size: 13px; color: #888; display: block; margin-bottom: 4px; }
.metric-value { font-size: 22px; font-weight: 700; color: #1890ff; }
.rank-history {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}
.rank-history .label { color: #888; }
.rank-val { margin-right: 12px; font-weight: 500; color: #333; }
.majors-section { margin-top: 12px; }
.majors-section h4 { font-size: 15px; margin-bottom: 8px; color: #555; }
.major-item {
  background: #fafafa;
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 8px;
}
.major-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.major-name { font-weight: 600; font-size: 15px; }
.major-score { margin-left: auto; font-size: 13px; color: #722ed1; font-weight: 500; }
.major-tags { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 6px; }
.subject-compare { display: flex; flex-wrap: wrap; gap: 12px; font-size: 13px; }
.subject-item { padding: 2px 8px; border-radius: 4px; }
.subject-item.above { background: #e6f7e9; color: #389e0d; }
.subject-item.below { background: #fff1f0; color: #cf1322; }
.risk-section { margin-top: 12px; }
</style>
