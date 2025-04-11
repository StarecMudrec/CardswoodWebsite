import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const userId = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const checkAuth = async () => {
    loading.value = true
    try {
      const response = await axios.get('http://localhost:8000/login?check_auth=true')
      isAuthenticated.value = response.data.isAuthenticated
      userId.value = response.data.userId
      return response.data
    } catch (err) {
      error.value = err.message
      isAuthenticated.value = false
      userId.value = null
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      await axios.get('http://localhost:8000/auth/logout', { withCredentials: true })
      isAuthenticated.value = false
      userId.value = null
    } catch (err) {
      error.value = err.message
    }
  }

  return { isAuthenticated, userId, loading, error, checkAuth, logout }
})