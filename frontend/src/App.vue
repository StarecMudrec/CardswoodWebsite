<template>
  <div id="app">
    <Navbar />
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
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

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-color);
  background-color: var(--bg-color);
  min-height: 100vh;
  padding: 0;
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
</style>
