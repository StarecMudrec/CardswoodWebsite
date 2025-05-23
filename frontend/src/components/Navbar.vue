<template>
  <div class="menu">
    <router-link to="/" class="nav-btn">CARDS</router-link>
    <router-link to="/termins" class="nav-btn">TERMINS</router-link>
    <a v-if="isAuthenticated" href="/auth/logout" class="nav-btn" @click.prevent="logout">LOGOUT</a>
    <router-link v-else to="/login" class="nav-btn">LOGIN</router-link>
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
  margin: 30px 0 50px 0;
  padding: 0;
  position: relative;
  z-index: 100;
}

.nav-btn {
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 500;
  font-size: 27px; /* Increased font size */
  letter-spacing: 1px; /* Slightly increased letter spacing for better readability with outline */
  position: relative;
  padding: 5px 0;
  transition: color 0.3s ease;
  text-stroke: 2px black;
}

.nav-btn:hover {
  color: var(--hover-color);
  text-shadow: none; /* Remove outline on hover for cleaner look */
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

@media (max-width: 768px) {
  .menu {
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .nav-btn {
    font-size: 16px;
  }
}
</style>
