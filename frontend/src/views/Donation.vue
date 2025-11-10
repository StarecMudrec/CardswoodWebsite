<template>
  <div class="donate-background">
    <div class="donate-view">
      <h1>Здесь скоро будет оплата...</h1>
      <!-- <p>This is the donate page content.</p> -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'DonationView'
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
  background-position: center 95%; /* Position the vertical center 80% down from the top, center horizontally */
  z-index: 1; /* Ensure it's behind the content */
}
.donate-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
