<template>
    <div class="login-container">
      <h1>Please log in</h1>
      <p>Only selected users may see this site.</p>
      <div id="telegram-login"></div>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { useAuthStore } from '../stores/auth'
  
  const authStore = useAuthStore()
  
  onMounted(() => {
    // Create script element
    const script = document.createElement('script')
    script.async = true
    script.src = 'https://telegram.org/js/telegram-widget.js?22'
    script.setAttribute('data-telegram-login', 'cardswoodwebbot')
    script.setAttribute('data-auth-url', 'http://localhost:8000/auth/telegram-callback')
    script.setAttribute('data-request-access', 'write')
    
    // Append to container
    const container = document.getElementById('telegram-login')
    container.appendChild(script)
  
    // Handle Telegram auth callback
    window.addEventListener('message', (event) => {
      if (event.data === 'auth-success') {
        authStore.checkAuth()
        window.location.href = '/home'
      }
    })
  })
  </script>
  
  <style scoped>
  .login-container {
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    max-width: 400px;
    margin: 0 auto;
  }
  
  #telegram-login {
    margin-top: 20px;
  }
  </style>