<template>
  <div class="donate-background page-with-navbar">
    <div class="donate-view">
      <h1 class="title">Платёж не завершён</h1>
      <p class="subtitle">
        Платёж был отменён или произошла ошибка. Вы можете попробовать снова в любое время.
      </p>
      <router-link to="/donate" class="home-link">Попробовать снова</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DonationFailView'
}
</script>

<style scoped>
.donate-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 95%;
  z-index: 1;
}

.donate-view {
  padding: 40px 20px;
  max-width: 600px;
  margin: 0 auto;
  color: #fff;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
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
}
</style>


