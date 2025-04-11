import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { setupAuthGuard } from './router/auth-guard'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Setup auth guard after router is installed
setupAuthGuard(router)

app.mount('#app')