<template>
    <div class="login-container">
      <iframe
        ref="loginIframe"
        src="http://localhost:80/login"
        frameborder="0"
        width="100%"
        height="100%"
        @load="handleIframeLoad"
      ></iframe>
    </div>
  </template>
  
  <script>
  console.log('Текущий домен:', window.location.origin);
  export default {
    name: 'LoginPage',
    data() {
      return {
        authChecked: false
      }
    },
    mounted() {
      // Обработчик сообщений от iframe
      window.addEventListener('message', this.handleAuthMessage);
      
      // Проверяем авторизацию при открытии страницы
      this.checkAuth();
    },
    beforeUnmount() {
      window.removeEventListener('message', this.handleAuthMessage);
    },
    methods: {
      handleIframeLoad() {
        console.log('Login iframe loaded');
        // Можно добавить дополнительную логику после загрузки
      },
      
      checkAuth() {
        // Отправляем запрос в iframe для проверки auth
        this.$refs.loginIframe.contentWindow.postMessage(
          { type: 'check-auth' },
          'http://localhost:80'
        );
      },
      
      handleAuthMessage(event) {
        // Проверяем источник сообщения
        if (event.origin !== 'http://localhost:80') return;
        
        // Обрабатываем разные типы сообщений
        switch (event.data.type) {
          case 'auth-status':
            this.handleAuthStatus(event.data.isAuthenticated);
            break;
          case 'auth-success':
            this.handleAuthSuccess();
            break;
        }
      },
      
      handleAuthStatus(isAuthenticated) {
        console.log('Auth status:', isAuthenticated);
        this.authChecked = true;
        
        if (isAuthenticated) {
          this.$router.push('/home');
        }
      },
      
      handleAuthSuccess() {
        console.log('Auth success, redirecting...');
        this.$router.push('/home');
      }
    }
  }
  </script>
  
  <style scoped>
  .login-container {
    width: 100%;
    height: 100vh;
    position: relative;
    overflow: hidden;
  }
  
  iframe {
    position: absolute;
    top: 0;
    left: 0;
    border: none;
  }
  </style>