<template>
  <div class="page-container">
    <div class="background-container" aria-hidden="true"></div>
    <img src="/logo_noph.png" alt="Логотип" class="background-logo">
    <div class="background-overlay" aria-hidden="true"></div>
    <div class="content-wrapper">
      <main class="result-section">
        <div class="result-card glass-effect">
          <div class="result-icon error-icon" aria-hidden="true">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41Z" fill="currentColor"/>
            </svg>
          </div>
          <h1 class="result-title">Ошибка оплаты</h1>
          <p class="result-text">Платёж не был завершён. Вы можете попробовать снова или вернуться в магазин.</p>
          <router-link to="/shop" class="back-link">Вернуться в магазин</router-link>
        </div>
      </main>
      <footer class="page-footer">
        <Footer />
      </footer>
    </div>
  </div>
</template>

<script>
import Footer from '@/components/Footer.vue'

export default {
  name: 'ShopFail',
  components: { Footer }
}
</script>

<style scoped>
.page-container,
.page-container * {
  font-family: "Tinos", serif !important;
}
.page-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
}
.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 450px;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%;
  z-index: 1;
  opacity: 0.7;
}
.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 450px;
  background: linear-gradient(to bottom, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.4) 100%);
  z-index: 1;
}
.background-logo {
  position: absolute;
  top: 120px;
  left: 50%;
  transform: translate(-50%, 0);
  width: 30vh;
  aspect-ratio: 1;
  z-index: 2;
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.5));
}
.content-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 1;
  z-index: 3;
}

.glass-effect {
  background: rgba(30, 30, 30, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.result-section {
  padding: 48px 16px 60px;
  width: min(480px, 100%);
  margin: 0 auto;
  margin-top: max(42vh, calc(120px + 30vh + 24px));
  text-align: center;
  color: #fff;
}

.result-card {
  padding: 40px 32px 36px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.result-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  flex-shrink: 0;
}

.result-icon.error-icon {
  color: #e57373;
  background: rgba(229, 115, 115, 0.2);
  border: 2px solid rgba(229, 115, 115, 0.5);
}

.result-title {
  font-size: 1.75rem;
  margin: 0;
  color: #e57373;
  letter-spacing: 0.02em;
}

.result-text {
  margin: 0;
  font-size: 1rem;
  line-height: 1.5;
  opacity: 0.9;
  color: rgba(255, 255, 255, 0.9);
}

.back-link {
  display: inline-block;
  margin-top: 8px;
  padding: 14px 28px;
  background: linear-gradient(135deg, rgba(255, 185, 71, 0.35), rgba(255, 185, 71, 0.2));
  color: #ffb947;
  text-decoration: none;
  border-radius: 12px;
  border: 1px solid rgba(255, 185, 71, 0.4);
  font-size: 1rem;
  font-weight: 600;
  transition: opacity 0.2s, transform 0.15s ease;
}

.back-link:hover {
  opacity: 0.95;
  transform: translateY(-1px);
}

.page-footer {
  position: relative;
  z-index: 3;
}
</style>
