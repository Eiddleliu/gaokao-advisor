import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/score-input',
    name: 'ScoreInput',
    component: () => import('../views/ScoreInput.vue'),
  },
  {
    path: '/recommendation',
    name: 'Recommendation',
    component: () => import('../views/Recommendation.vue'),
  },
  {
    path: '/universities',
    name: 'UniversityList',
    component: () => import('../views/UniversityList.vue'),
  },
  {
    path: '/university/:id',
    name: 'UniversityDetail',
    component: () => import('../views/UniversityDetail.vue'),
    props: true,
  },
  {
    path: '/volunteer-plan',
    name: 'VolunteerPlan',
    component: () => import('../views/VolunteerPlan.vue'),
  },
  {
    path: '/score-query',
    name: 'ScoreQuery',
    component: () => import('../views/ScoreQuery.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
