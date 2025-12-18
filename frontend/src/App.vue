<template>
  <div id="app">
    <Navbar :user="user"/>
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <div class="user-info" v-if="user">
      <!-- <img :src="'/proxy/avatar?url=' + encodeURIComponent(user.photo_url)" alt="User Avatar" class="avatar">
      <span class="username">
        {{ user.first_name }} {{ user.last_name }}
      </span> -->
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // Import axios
import Navbar from '@/components/Navbar.vue'
import router from './router'; // Import router

export default {
  name: 'App',
  components: { Navbar },
  data() {
    return {
      user: null // Initialize user data to null
    };
  },
  mounted() {
    // Make a GET request to the user endpoint on component mount
    axios.get('/api/user')
      .then(response => {
        if (response.status === 200 && response.data) {
          this.user = response.data; // Set the user data if authenticated
        } else {
          this.user = null; // Ensure user is null if not authenticated
        }
      })
      .catch(error => {
        console.error('Ошибка получения данных пользователя:', error);
        this.user = null; // Ensure user is null on error
      });
  },
}
</script>

<style>
/* Theme variables and global helpers */
:root {
  --bg-color: #121212;
  --card-bg: #1e1e1e;
  --text-color: #e0e0e0;
  --accent-color: #ffffff;
  --hover-color: #b3b3b3;
  --hover-border-color: #777777;
  --card-border-color: #bebebe;
  --font-family-main: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

* {
  box-sizing: border-box;
}

/* Page transition */
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
  z-index: 10;
}

.user-info .avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
  border: 1px solid var(--card-border-color);
  object-fit: cover;
}

button,
.button {
  padding: 10px 15px;
  font-family: var(--font-family-main);
}
</style>
