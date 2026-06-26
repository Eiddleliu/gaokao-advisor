import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useScoreStore = defineStore('score', () => {
  // 考生信息
  const scoreInput = ref({
    province: '山东',
    exam_type: '新高考3+3',
    batch: '本科批',
    year: 2026,
    total_score: null,
    rank: null,
    chinese: null,
    math: null,
    english: null,
    physics: null,
    chemistry: null,
    biology: null,
    politics: null,
    history: null,
    geography: null,
    // 偏好
    city_preference: [],
    public_only: false,
    max_tuition: null,
    accept_adjustment: true,
    excluded_majors: [],
    career_goal: null,
    special_type: null,
  })

  // 推荐结果
  const recommendResult = ref(null)
  const recommendLoading = ref(false)

  // 志愿方案
  const volunteerPlans = ref([])
  const currentPlan = ref(null)

  // 计算属性：优势科目和短板科目
  const subjectAnalysis = computed(() => {
    const subjects = []
    const s = scoreInput.value
    const items = [
      { name: '语文', score: s.chinese, full: 150 },
      { name: '数学', score: s.math, full: 150 },
      { name: '英语', score: s.english, full: 150 },
      { name: '物理', score: s.physics, full: 100 },
      { name: '化学', score: s.chemistry, full: 100 },
      { name: '生物', score: s.biology, full: 100 },
      { name: '政治', score: s.politics, full: 100 },
      { name: '历史', score: s.history, full: 100 },
      { name: '地理', score: s.geography, full: 100 },
    ]
    for (const item of items) {
      if (item.score != null) {
        const ratio = item.score / item.full
        subjects.push({
          ...item,
          ratio,
          level: ratio >= 0.85 ? 'strong' : ratio >= 0.70 ? 'medium' : 'weak',
        })
      }
    }
    subjects.sort((a, b) => b.ratio - a.ratio)
    return subjects
  })

  const strongSubjects = computed(() =>
    subjectAnalysis.value.filter(s => s.level === 'strong')
  )
  const weakSubjects = computed(() =>
    subjectAnalysis.value.filter(s => s.level === 'weak')
  )

  function resetScore() {
    scoreInput.value = {
      province: '山东', exam_type: '新高考3+3', batch: '本科批', year: 2026,
      total_score: null, rank: null,
      chinese: null, math: null, english: null,
      physics: null, chemistry: null, biology: null,
      politics: null, history: null, geography: null,
      city_preference: [], public_only: false, max_tuition: null,
      accept_adjustment: true, excluded_majors: [],
      career_goal: null, special_type: null,
    }
    recommendResult.value = null
  }

  return {
    scoreInput, recommendResult, recommendLoading,
    volunteerPlans, currentPlan,
    subjectAnalysis, strongSubjects, weakSubjects,
    resetScore,
  }
})
