<template>
  <div id="app">
    <Navbar />
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <div class="user-info">
      <img src="@/assets/default-avatar.png" alt="User Avatar" class="avatar">
      <span class="username">Username</span>
    </router-view>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'

export default {
  components: {
    Navbar
  }
}
</script>

<style>
/* Глобальные стили */
:root {
  --bg-color: #121212;
  --card-bg: #1e1e1e;
  --text-color: #e0e0e0;
  --accent-color: #ffffff;
  --hover-color: #bb86fc;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  background-color: var(--bg-color);
}

.global-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  align-items: center;
  margin: 0;
}

/* Убираем стандартные отступы браузера */
body {
  margin: 0;
  padding: 0;
}

/* Анимации переходов */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.user-info {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  align-items: center;
  color: var(--text-color);
  font-size: 14px;
}

.user-info .avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
  border: 1px solid var(--border-color);
  object-fit: cover; /* Ensure the image covers the area without distortion */
}

</style>
