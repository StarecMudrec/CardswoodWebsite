<template>
  <div class="login-container">
    <h1>Please log in</h1>
    <p>Only selected users may access this site.</p>

    <div ref="telegramWidget"></div>

    <router-link to="/" class="back-link">← Back to home</router-link>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'

export default {
  setup() {
    const telegramWidget = ref(null)

    onMounted(() => {
      // Dynamically load the Telegram widget script
      const script = document.createElement('script')
      script.async = true
      script.src = 'https://telegram.org/js/telegram-widget.js?22'
      script.dataset.telegramLogin = 'cardswoodwebbot'
      script.dataset.authUrl = 'https://cardswood.ru/auth/telegram-callback'
      script.dataset.requestAccess = 'write'
      
      // Add the script to our container div
      telegramWidget.value.appendChild(script)

      // Handle auth success message
      window.addEventListener('message', handleAuthMessage)
    })
    
    const handleAuthMessage = (event) => {
      if (event.data === 'auth-success') {
        window.location.href = '/' // Or use Vue Router if needed
      }
    }
    
    return {
      telegramWidget
    }
  }
}
</script>

<style scoped>
.login-container {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background-color: var(--card-bg);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  margin: 40px auto;
  text-align: center;
}

h1 {
  color: var(--accent-color);
  font-weight: 500;
  margin-bottom: 15px;
  font-size: 24px;
}

p {
  margin-bottom: 30px;
  color: #aaa;
  font-size: 16px;
}

.back-link {
  display: inline-block;
  margin-top: 25px;
  color: var(--accent-color);
  text-decoration: none;
  font-size: 14px;
  position: relative;
  padding-bottom: 2px;
}

.back-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: var(--accent-color);
  transition: width 0.3s ease;
}

.back-link:hover::after {
  width: 100%;
}

@media (max-width: 480px) {
  .login-container {
    padding: 30px 20px;
    margin: 0 15px;
  }
  
  h1 {
    font-size: 20px;
  }
  
  p {
    font-size: 14px;
  }
}
</style>
