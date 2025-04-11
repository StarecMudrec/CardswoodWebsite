<template>
    <div class="navbar">
      <p>Menu: 
        <router-link to="/home">CARDS</router-link> | 
        <router-link to="/termins">TERMINS</router-link> | 
        <a v-if="authStore.isAuthenticated" href="#" @click.prevent="handleLogout">LOGOUT</a>
        <router-link v-else to="/login">LOGIN</router-link>
      </p>
    </div>
  </template>
  
  <script setup>
  import { useAuthStore } from '../stores/auth'
  import { useRouter } from 'vue-router'
  
  const authStore = useAuthStore()
  const router = useRouter()
  
  const handleLogout = async () => {
    await authStore.logout()
    router.push('/home')
  }
  </script>
  
  <style scoped>
  .navbar {
    margin-bottom: 20px;
  }
  a {
    margin: 0 5px;
    color: inherit;
    text-decoration: none;
  }
  a:hover {
    text-decoration: underline;
  }
  .router-link-active {
    font-weight: bold;
  }
  </style>