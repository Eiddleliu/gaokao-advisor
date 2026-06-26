import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// 智能推荐
export const generateRecommendation = (data) =>
  api.post('/recommend/generate', data)

export const checkSubjectRisk = (data) =>
  api.post('/recommend/check-subject-risk', data)

// 院校查询
export const listUniversities = (params) =>
  api.get('/university/list', { params })

export const getUniversityDetail = (id) =>
  api.get(`/university/${id}`)

export const getUniversityMajors = (id, params) =>
  api.get(`/university/${id}/majors`, { params })

export const getMajorDetail = (id) =>
  api.get(`/university/major/${id}`)

export const getUniversityAdmissions = (id, params) =>
  api.get(`/university/${id}/admissions`, { params })

// 志愿规划
export const createVolunteerPlan = (data) =>
  api.post('/volunteer/plan', data)

export const listVolunteerPlans = (userId) =>
  api.get(`/volunteer/plans/${userId}`)

export const getVolunteerPlan = (planId) =>
  api.get(`/volunteer/plan/${planId}`)

export const checkVolunteerRisk = (choices) =>
  api.post('/volunteer/risk-check', choices)

// 分数查询
export const getScoreSegments = (params) =>
  api.get('/score/segments', { params })

export const getBatchLines = (params) =>
  api.get('/score/batch-lines', { params })

export const getEquivalentScore = (params) =>
  api.get('/score/equivalent-score', { params })

export default api
