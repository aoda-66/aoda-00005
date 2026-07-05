import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Dashboard',
    redirect: '/books',
    meta: { requiresAuth: true }
  },
  {
    path: '/books',
    name: 'Books',
    component: () => import('../views/Books.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/damages',
    name: 'Damages',
    component: () => import('../views/Damages.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/procedures',
    name: 'Procedures',
    component: () => import('../views/Procedures.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/materials',
    name: 'Materials',
    component: () => import('../views/Materials.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/archives',
    name: 'Archives',
    component: () => import('../views/Archives.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/Users.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/roles',
    name: 'Roles',
    component: () => import('../views/Roles.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.meta.requiresAuth !== false
  
  if (requiresAuth && !token) {
    next('/login')
  } else if (!requiresAuth && token && to.path === '/login') {
    next('/books')
  } else {
    next()
  }
})

export default router