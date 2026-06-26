<template>
  <div class="score-input-page">
    <h1 class="page-title">考生信息录入</h1>
    <p class="page-subtitle">请准确填写你的高考各科分数和偏好，系统将根据单科优势为你精准推荐</p>

    <el-form :model="form" label-width="110px" class="input-form card">
      <!-- 基本信息 -->
      <el-divider content-position="left">基本信息</el-divider>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="省份">
            <el-select v-model="form.province" placeholder="选择省份">
              <el-option v-for="p in provinces" :key="p" :label="p" :value="p" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="高考类型">
            <el-select v-model="form.exam_type">
              <el-option label="新高考 3+3" value="新高考3+3" />
              <el-option label="新高考 3+1+2" value="新高考3+1+2" />
              <el-option label="传统文理" value="传统文理" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="批次">
            <el-select v-model="form.batch">
              <el-option label="本科批" value="本科批" />
              <el-option label="本科提前批" value="本科提前批" />
              <el-option label="专科批" value="专科批" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="总分" required>
            <el-input-number v-model="form.total_score" :min="0" :max="750" :step="1" controls-position="right" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="全省位次" required>
            <el-input-number v-model="form.rank" :min="1" :max="1000000" :step="100" controls-position="right" />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 单科分数 -->
      <el-divider content-position="left">单科成绩（核心竞争力）</el-divider>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="语文">
            <el-input-number v-model="form.chinese" :min="0" :max="150" controls-position="right" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="数学">
            <el-input-number v-model="form.math" :min="0" :max="150" controls-position="right" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="英语">
            <el-input-number v-model="form.english" :min="0" :max="150" controls-position="right" />
          </el-form-item>
        </el-col>
      </el-row>

      <p class="section-hint">选科成绩（根据你所在省份的高考类型填写）</p>
      <el-row :gutter="20" v-if="form.exam_type !== '传统文理'">
        <el-col :span="8">
          <el-form-item label="物理">
            <el-input-number v-model="form.physics" :min="0" :max="100" controls-position="right" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="化学">
            <el-input-number v-model="form.chemistry" :min="0" :max="100" controls-position="right" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="生物">
            <el-input-number v-model="form.biology" :min="0" :max="100" controls-position="right" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="政治">
            <el-input-number v-model="form.politics" :min="0" :max="100" controls-position="right" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="历史">
            <el-input-number v-model="form.history" :min="0" :max="100" controls-position="right" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="地理">
            <el-input-number v-model="form.geography" :min="0" :max="100" controls-position="right" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20" v-else>
        <el-col :span="8">
          <el-form-item label="理综">
            <el-input-number v-model="form.comprehensive_science" :min="0" :max="300" controls-position="right" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="文综">
            <el-input-number v-model="form.comprehensive_arts" :min="0" :max="300" controls-position="right" />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 单科分析提示 -->
      <div v-if="scoreStore.subjectAnalysis.length > 0" class="subject-analysis card-inline">
        <h4>单科分析</h4>
        <div class="subject-tags">
          <el-tag v-for="s in scoreStore.strongSubjects" :key="s.name" type="success" size="large" class="subject-tag">
            {{ s.name }} {{ s.score }}分 - 优势科目
          </el-tag>
          <el-tag v-for="s in scoreStore.weakSubjects" :key="s.name" type="danger" size="large" class="subject-tag">
            {{ s.name }} {{ s.score }}分 - 相对薄弱
          </el-tag>
        </div>
        <p class="hint-text" v-if="scoreStore.strongSubjects.length > 0">
          推荐方向：{{ getRecommendHint() }}
        </p>
      </div>

      <!-- 偏好设置 -->
      <el-divider content-position="left">筛选偏好（可选）</el-divider>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="城市偏好">
            <el-select v-model="form.city_preference" multiple placeholder="不限（可选多个城市）" style="width:100%">
              <el-option v-for="c in cities" :key="c" :label="c" :value="c" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="只看公办">
            <el-switch v-model="form.public_only" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="学费上限">
            <el-input-number v-model="form.max_tuition" :min="0" :step="5000" :max="100000" controls-position="right" placeholder="不限" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="排除专业">
            <el-select v-model="form.excluded_majors" multiple placeholder="不排除任何专业" style="width:100%">
              <el-option v-for="m in majorCategories" :key="m" :label="m" :value="m" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="长期规划">
            <el-select v-model="form.career_goal" placeholder="不限" clearable>
              <el-option label="考研优先" value="考研" />
              <el-option label="考公优先" value="考公" />
              <el-option label="就业高薪" value="就业" />
              <el-option label="出国深造" value="出国" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="接受调剂">
            <el-switch v-model="form.accept_adjustment" />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 提交 -->
      <el-form-item style="margin-top: 24px;">
        <el-button type="primary" size="large" @click="submitRecommendation" :loading="loading" style="width: 200px;">
          生成智能推荐方案
        </el-button>
        <el-button size="large" @click="fillDemo">填入示例数据</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useScoreStore } from '../stores/score'
import { generateRecommendation } from '../api'

const router = useRouter()
const scoreStore = useScoreStore()
const loading = ref(false)
const form = reactive(scoreStore.scoreInput)

const provinces = ['山东', '北京', '上海', '江苏', '浙江', '广东', '湖北', '四川', '河南', '河北', '湖南', '安徽', '福建', '陕西', '辽宁']
const cities = ['北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都', '西安', '长沙', '青岛', '天津', '重庆', '厦门']
const majorCategories = ['工学', '理学', '医学', '文学', '经济学', '管理学', '法学', '教育学', '艺术学', '农学']

function getRecommendHint() {
  const strong = scoreStore.strongSubjects.map(s => s.name)
  const hints = []
  if (strong.includes('数学')) hints.push('工科、经管类、统计学')
  if (strong.includes('物理')) hints.push('电子信息、机械、自动化')
  if (strong.includes('英语')) hints.push('外语类、国际商务、翻译')
  if (strong.includes('化学')) hints.push('化工、材料、药学')
  if (strong.includes('生物')) hints.push('生物科学、医学、农学')
  if (strong.includes('语文')) hints.push('中文、新闻、法学')
  return hints.length ? hints.join('；') : '根据综合分数推荐'
}

function fillDemo() {
  Object.assign(form, {
    province: '山东', exam_type: '新高考3+3', batch: '本科批',
    total_score: 600, rank: 25000,
    chinese: 115, math: 130, english: 95,
    physics: 82, chemistry: 78, biology: 70,
  })
}

async function submitRecommendation() {
  if (!form.total_score || !form.rank) {
    ElMessage.warning('请填写总分和全省位次')
    return
  }
  loading.value = true
  try {
    const resp = await generateRecommendation({
      score: { ...form },
      strategy: 'balanced',
      limit: 20,
    })
    scoreStore.recommendResult = resp.data
    router.push('/recommendation')
  } catch (e) {
    ElMessage.error('推荐生成失败：' + (e.response?.data?.detail || e.message))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.input-form { max-width: 960px; margin: 0 auto; }
.section-hint { color: #888; font-size: 14px; margin-bottom: 12px; padding-left: 110px; }
.subject-analysis {
  background: #f0f7ff;
  border: 1px solid #d4e8ff;
  border-radius: 8px;
  padding: 16px 20px;
  margin: 0 0 20px 110px;
}
.subject-analysis h4 { margin-bottom: 8px; color: #1890ff; }
.subject-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }
.subject-tag { font-size: 14px; }
.hint-text { font-size: 14px; color: #52c41a; margin-top: 8px; }
.card-inline { background: #f0f7ff; }
</style>
