<template>
  <div class="menu">
    <router-link to="/" class="nav-btn" data-text="CARDS">CARDS</router-link>
    <router-link to="/termins" class="nav-btn" data-text="TERMINS">TERMINS</router-link>
    <a v-if="isAuthenticated" href="/auth/logout" class="nav-btn" data-text="LOGOUT" @click.prevent="logout">LOGOUT</a>
    <router-link v-else to="/login" class="nav-btn" data-text="LOGIN">LOGIN</router-link>
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
  font-weight: 700;
  font-size: 27px; /* Base font size */
  -webkit-text-stroke: 1.2px black; /* Apply the black stroke */
  letter-spacing: 1px;
  position: relative;
  padding: 5px 0;
  transition: color 0.3s ease;
}

.nav-btn:hover {
  color: var(--hover-color);
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

@media (max-width: 768px) { /* Media query for smaller screens */
  .menu {
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .nav-btn {
    font-size: 16px;
  }
}
</style>
