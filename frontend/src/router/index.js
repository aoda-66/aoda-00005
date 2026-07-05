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
    name: 'Layout',
    component: () => import('../components/Layout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
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
      },
      {
        path: '/users',
        name: 'Users',
        component: () => import('../views/Users.vue')
      },
      {
        path: '/roles',
        name: 'Roles',
        component: () => import('../views/Roles.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)
  
  if (requiresAuth && !token) {
    next('/login')
  } else if (!requiresAuth && token && to.path === '/login') {
    next('/books')
  } else {
    next()
  }
})

export default router