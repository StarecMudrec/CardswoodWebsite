<template>
  <div>
    <div class="background-container"></div>
    <img src="/logo_noph.png" alt="Logo" class="background-logo">
    <hr class="separator-line">
    <div id="seasons-container">
      <div v-if="loading" class="loading">Loading cards...</div>
      <div v-else-if="error" class="error-message">Error loading data: {{ error.message || error }}. Please try again later.</div>
      <div v-else-if="seasons.length === 0" class="loading">No seasons found</div>
      <Season 
        v-for="season in seasons" 
        :key="season.uuid" 
        :season="season" 
        @card-clicked="navigateToCard"
        @add-card="navigateToAddCard"
        @card-deleted="handleCardDeleted"
      />
    </div>
  </div>

</template>

<style scoped>
.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px; /* Adjust height as needed */
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%; /* Position the vertical center 80% down from the top, center horizontally */
  z-index: 1; /* Ensure it's behind the content */
}

.background-logo {
  position: absolute;
  top: 100px;
  left: 50%;
  transform: translate(-50%, 0);
  max-width: 250px; /* Adjust size as needed */
  max-height: 250px; /* Adjust size as needed */
  z-index: 1; /* Ensure it's behind the content */
}

.separator-line {
  position: relative;
  margin-top: 370px; /* Adjust to be below the background image */
  height: 2px;
  background-color: white;
  border: none;
  z-index: 2; /* Ensure it's above the background */
  width: 75%;
}

#seasons-container {
  position: relative; /* Essential for z-index to work correctly relative to the background */
  margin-top: 30px; /* Push content down by the height of the background */
  z-index: 2; /* Ensure content is above the background */
  /* Add other styles for your seasons container here */
  padding-bottom: 50px;
}
.error-message {
  text-align: center;
  margin: 50px 0;
  color: #ff5555; /* Red color for errors */
}
</style>

<script>
import Season from '@/components/Season.vue'
import { mapActions, mapState } from 'vuex'

export default {
  components: {
    Season
  },
  computed: {
    ...mapState(['seasons', 'loading', 'error'])
  },
  methods: {
    ...mapActions(['fetchSeasons']),
    navigateToCard(cardUuid) {
 this.$router.push(`/card/${cardUuid}`)
    },
    async handleCardDeleted(deletedCardUuid) {
      try {
        // Assuming you have an axios instance configured globally or imported
        await this.$axios.delete(`/api/cards/${deletedCardUuid}`);
        console.log(`Card with UUID ${deletedCardUuid} deleted successfully`);
        
        // Update the seasons state to remove the deleted card
        // This requires modifying how seasons and cards are managed in the store
        // For simplicity, this example refetches seasons.
        // A more efficient approach would be to mutate the store state directly.
        this.fetchSeasons(); 
      } catch (error) {
        console.error(`Error deleting card with UUID ${deletedCardUuid}:`, error);
        alert('Failed to delete card: ' + (error.response?.data?.error || error.message));
      }
    },
  },
  mounted() {
    this.fetchSeasons()
  },
}
</script>