<template>
  <router-view />
</template>

<script setup>
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

// Check auth status when app loads
authStore.checkAuth()
</script>