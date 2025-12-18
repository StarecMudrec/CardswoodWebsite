<template>
  <div class="page-container">
    <div class="background-container"></div>
    <img src="/logo_noph.png" alt="Логотип" class="background-logo">
    <hr class="separator-line">

    <div class="content-wrapper">
      <section class="donate-section">
        <div class="card fail-card">
          <h1 class="title">Платёж не завершён</h1>
          <p class="subtitle">
            Платёж был отменён или произошла ошибка. Вы можете попробовать снова в любое время.
          </p>
          <router-link to="/donate" class="home-link">Попробовать снова</router-link>
        </div>
      </section>

      <Footer />
    </div>
  </div>
</template>

<script>
import Footer from '@/components/Footer.vue'

export default {
  name: 'DonationFailView',
  components: {
    Footer
  }
}
</script>

<style scoped>
.page-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%;
  z-index: 1;
}

.background-logo {
  position: absolute;
  top: 100px;
  left: 50%;
  transform: translate(-50%, 0);
  max-width: 250px;
  max-height: 250px;
  z-index: 1;
}

.separator-line {
  position: relative;
  margin-top: 47vh;
  height: 2px;
  background-color: white;
  border: none;
  z-index: 2;
  width: 75%;
}

.content-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 1;
  z-index: 2;
}

.donate-section {
  padding: 32px 16px 40px;
  width: min(720px, 100%);
  margin: 0 auto;
  color: var(--text-color, #fff);
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

.card {
  background: radial-gradient(circle at top left, rgba(255, 185, 71, 0.12), transparent 55%),
    rgba(0, 0, 0, 0.75);
  border-radius: 18px;
  padding: 26px 22px 24px;
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  text-align: center;
}

.title {
  font-size: 42px;
  margin-bottom: 10px;
}

.subtitle {
  margin-bottom: 24px;
  font-size: 18px;
}

.home-link {
  display: inline-block;
  margin-top: 10px;
  color: #ffb947;
  text-decoration: none;
  font-weight: 500;
}

@media (max-width: 1024px) {
  .separator-line {
    width: 90%;
  }
}

@media (max-width: 768px) {
  .background-logo {
    max-width: 200px;
    max-height: 200px;
    top: 90px;
  }

  .separator-line {
    margin-top: 42vh;
  }

  .donate-section {
    padding-inline: 12px;
  }

  .title {
    font-size: 32px;
  }

  .subtitle {
    font-size: 16px;
  }
}

@media (max-width: 600px) {
  .title {
    font-size: 28px;
  }

  .card {
    padding: 20px 16px 18px;
  }
}
</style>
