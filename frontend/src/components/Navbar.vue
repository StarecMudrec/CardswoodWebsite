<template>
  <header class="navbar">
    <div class="navbar-inner">
      <router-link to="/" class="navbar-logo">
        CARDSWOOD
      </router-link>

      <nav class="menu" aria-label="Основная навигация">
        <router-link to="/" class="nav-btn" exact-active-class="nav-btn-active">КАРТОЧКИ</router-link>
        <router-link to="/donate" class="nav-btn" active-class="nav-btn-active">ПОДДЕРЖАТЬ</router-link>
        <a
          v-if="isAuthenticated"
          href="/auth/logout"
          class="nav-btn"
          @click.prevent="logout"
        >
          ВЫЙТИ
        </a>
        <router-link v-else to="/login" class="nav-btn" active-class="nav-btn-active">ВОЙТИ</router-link>
      </nav>
    </div>
  </header>
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
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  backdrop-filter: blur(14px);
  background: linear-gradient(
      to bottom,
      rgba(10, 10, 10, 0.92),
      rgba(10, 10, 10, 0.75),
      rgba(10, 10, 10, 0.4)
  );
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.navbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-logo {
  font-weight: 600;
  letter-spacing: 0.16em;
  font-size: 16px;
  color: var(--accent-color);
  text-decoration: none;
  text-transform: uppercase;
  opacity: 0.9;
}

.menu {
  display: flex;
  justify-content: center;
  gap: 24px;
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

.nav-btn-active {
  color: var(--hover-color);
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
  .nav-btn {
    font-size: 15px;
  }

  .navbar-inner {
    padding-inline: 14px;
  }

  .menu {
    gap: 16px;
  }
}
</style>
