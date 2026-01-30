<template>
  <div class="page-container">
    <div class="background-container" aria-hidden="true"></div>
    <img src="/logo_noph.png" alt="Логотип" class="background-logo">
    <div class="background-overlay" aria-hidden="true"></div>
    <div class="content-wrapper">
      <main class="result-section">
        <h1 class="result-title">Оплата прошла успешно</h1>
        <p class="result-text">Спасибо за покупку. Товары будут зачислены в ваш аккаунт.</p>
        <router-link to="/shop" class="back-link">Вернуться в магазин</router-link>
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
  name: 'ShopSuccess',
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
.result-section {
  padding: 48px 16px 60px;
  width: min(600px, 100%);
  margin: 0 auto;
  margin-top: 40vh;
  text-align: center;
  color: #fff;
}
.result-title {
  font-size: 1.75rem;
  margin-bottom: 16px;
  color: #ffb947;
}
.result-text {
  margin-bottom: 24px;
  opacity: 0.9;
}
.back-link {
  display: inline-block;
  padding: 12px 24px;
  background: linear-gradient(135deg, rgba(255, 185, 71, 0.3), rgba(255, 185, 71, 0.15));
  color: #ffb947;
  text-decoration: none;
  border-radius: 8px;
  transition: opacity 0.2s;
}
.back-link:hover {
  opacity: 0.9;
}
.page-footer {
  position: relative;
  z-index: 3;
}
</style>
