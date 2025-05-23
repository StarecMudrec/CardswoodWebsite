<template>
  <div class="home-container">
    <div class="background-container">
      <!-- The background image will be applied here -->
    </div>
    <div id="seasons-container">
      <div v-if="loading" class="loading">Loading cards...</div>
      <div v-else-if="error" class="loading" style="color: #ff5555;">Error loading data. Please try again later.</div>
      <div v-else-if="seasons.length === 0" class="loading">No seasons found</div>
      <Season 
        v-for="season in seasons" 
        :key="season.uuid" 
        :season="season" 
        @card-clicked="navigateToCard"
      />
    </div>
  </div>

</template>

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
    }
  },
  created() {
    this.fetchSeasons()
  }
}
</script>


<style scoped>
.home-container {
  position: relative; /* Needed for absolute positioning of the background */
}

.background-container {
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: top center;
  height: 400px; /* Adjust this height as needed */
  width: 100%;
  position: absolute; /* Position over other content */
  top: 0;
  left: 0;
  z-index: 1; /* Ensure it's behind the content */
}

 #seasons-container {
  margin-top: 420px; /* Adjust this value to be at least the height of the background */
  z-index: 2; /* Ensure it's above the background */
}
</style>