<template>
  <div class="menu">
    <router-link to="/" class="nav-btn">КАРТОЧКИ</router-link>
    <router-link to="/donate" class="nav-btn">ВИТРИНА</router-link>
    <a v-if="isAuthenticated" href="/auth/logout" class="nav-btn" @click.prevent="logout">ВЫЙТИ</a>
    <router-link v-else to="/login" class="nav-btn">ВОЙТИ</router-link>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['isAuthenticated'])
  },
  methods: {
    async logout() {
      await this.$store.dispatch('logout')
      // Перенаправление уже обрабатывается в роутере
    }
  }
}
</script>

<style scoped>
.menu {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 0;
  padding: 18px 0;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: transparent;
  pointer-events: auto;
}

.nav-btn {
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 500;
  font-size: 25px; /* Increased font size */
  letter-spacing: 1px; /* Slightly increased letter spacing for better readability with outline */
  position: relative;
  padding: 5px 0;
  transition: color 0.3s ease, box-shadow 0.3s ease; /* Add box-shadow to transition */
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Semi-transparent dark shadow */
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.nav-btn:hover {
  color: var(--hover-color);
  -webkit-text-stroke: 0.15px var(--hover-border-color);
  transition: color 0.3s ease, box-shadow 0.3s ease; /* Add box-shadow to transition */
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Semi-transparent dark shadow */
}

.nav-btn::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: var(--hover-color);
  transition: width 0.3s ease;
}

.nav-btn:hover::after {
  width: 100%;
}

@media (max-width: 480px) {
  .menu {
    gap: 20px;
    padding: 14px 0;
  }
  
  .nav-btn {
    font-size: 16px;
  }
}
</style>
