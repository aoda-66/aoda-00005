import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    redirect: '/books'
  },
  {
    path: '/books',
    name: 'Books',
    component: () => import('../views/Books.vue')
  },
  {
    path: '/damages',
    name: 'Damages',
    component: () => import('../views/Damages.vue')
  },
  {
    path: '/procedures',
    name: 'Procedures',
    component: () => import('../views/Procedures.vue')
  },
  {
    path: '/materials',
    name: 'Materials',
    component: () => import('../views/Materials.vue')
  },
  {
    path: '/archives',
    name: 'Archives',
    component: () => import('../views/Archives.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router