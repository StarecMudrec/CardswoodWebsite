import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  // Добавьте другие маршруты по аналогии
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Обработчик проверки авторизации
router.beforeEach((to, from, next) => {
  const isAuthenticated = /* ваша логика проверки auth */ false
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router