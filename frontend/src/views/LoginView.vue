<template>
    <div class="login-view">
      <NavBar />
      <TelegramLogin />
    </div>
  </template>
  
  <script setup>
  import NavBar from '../components/NavBar.vue'
  import TelegramLogin from '../components/TelegramLogin.vue'
  import { useAuthStore } from '../stores/auth'
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  
  const authStore = useAuthStore()
  const router = useRouter()
  
  onMounted(async () => {
    await authStore.checkAuth()
    if (authStore.isAuthenticated) {
      router.push('/home')
    }
  })
  </script>
  
  <style scoped>
  .login-view {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background: #f5f5f5;
    padding: 20px;
  }
  </style>