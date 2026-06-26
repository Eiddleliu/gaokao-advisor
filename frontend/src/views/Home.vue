<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1>不止看总分<br/>按单科强项匹配最适合你的大学专业</h1>
        <p class="hero-desc">
          全国首个基于单科分数加权匹配的高考志愿推荐系统。<br/>
          录入语数外+选科成绩，智能分析你的单科优势，精准推荐适配院校专业。
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="$router.push('/score-input')">
            开始智能推荐
          </el-button>
          <el-button size="large" @click="$router.push('/universities')">
            浏览院校库
          </el-button>
        </div>
      </div>
    </section>

    <!-- Feature Cards -->
    <section class="features">
      <div class="feature-card" v-for="feature in features" :key="feature.title">
        <div class="feature-icon">{{ feature.icon }}</div>
        <h3>{{ feature.title }}</h3>
        <p>{{ feature.desc }}</p>
      </div>
    </section>

    <!-- How it works -->
    <section class="how-it-works card">
      <h2>推荐原理</h2>
      <div class="steps">
        <div class="step">
          <div class="step-num">1</div>
          <h4>位次初筛</h4>
          <p>根据全省位次，按冲/稳/保梯度匹配候选院校，确保符合投档规则</p>
        </div>
        <div class="step">
          <div class="step-num">2</div>
          <h4>单科加权</h4>
          <p>对每个专业设置单科权重，如计算机看重数学40%、物理30%，精准匹配你的强项</p>
        </div>
        <div class="step">
          <div class="step-num">3</div>
          <h4>智能排序</h4>
          <p>综合位次匹配度和单科适配度，优先推荐你最有优势、最适合的院校专业</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const features = [
  { icon: '📊', title: '单科精准匹配', desc: '录入每科成绩，按专业单科权重打分，找到你的强项对应的最佳专业方向' },
  { icon: '🎯', title: '冲稳保三档规划', desc: '基于位次梯度科学划分冲刺、稳妥、保底院校，杜绝滑档风险' },
  { icon: '⚠️', title: '风险预警检测', desc: '自动检测单科门槛、调剂风险、梯度不合理等问题，为志愿保驾护航' },
  { icon: '📋', title: '一键生成志愿表', desc: '根据本省志愿数量上限，自动生成完整志愿方案，支持多方案对比' },
]
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 80px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
  margin-bottom: 32px;
}
.hero h1 {
  font-size: 36px;
  font-weight: 800;
  line-height: 1.4;
  margin-bottom: 16px;
}
.hero-desc {
  font-size: 16px;
  opacity: 0.9;
  line-height: 1.8;
  margin-bottom: 32px;
}
.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}
.features {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}
.feature-card {
  background: white;
  border-radius: 12px;
  padding: 28px 20px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  transition: transform 0.2s;
}
.feature-card:hover { transform: translateY(-4px); }
.feature-icon { font-size: 40px; margin-bottom: 12px; }
.feature-card h3 { font-size: 17px; margin-bottom: 8px; color: #1a1a2e; }
.feature-card p { font-size: 14px; color: #666; line-height: 1.6; }
.how-it-works h2 { font-size: 22px; margin-bottom: 24px; color: #1a1a2e; }
.steps { display: flex; gap: 24px; }
.step { flex: 1; text-align: center; }
.step-num {
  width: 48px; height: 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: bold;
  margin: 0 auto 12px;
}
.step h4 { margin-bottom: 8px; color: #333; }
.step p { font-size: 14px; color: #666; line-height: 1.6; }

@media (max-width: 768px) {
  .features { grid-template-columns: repeat(2, 1fr); }
  .steps { flex-direction: column; }
  .hero h1 { font-size: 26px; }
}
</style>
