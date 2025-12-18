<template>
  <div class="donate-background page-with-navbar">
    <div class="donate-view">
      <h1 class="title">Спасибо!</h1>
      <p class="subtitle">
        Платёж получен. Спасибо за поддержку!
      </p>
      <router-link to="/" class="home-link">Вернуться к карточкам</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DonationSuccessView'
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


