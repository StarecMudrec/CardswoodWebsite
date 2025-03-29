import { useAuthStore } from '../stores/auth'

export async function setupAuthGuard(router) {
  const authStore = useAuthStore()
  
  router.beforeEach(async (to, from, next) => {
    await authStore.checkAuth()
    next()
  })
}