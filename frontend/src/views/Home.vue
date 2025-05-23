<template>
  <div>
    <div id="seasons-container">
      <div v-if="loading" class="loading">Loading cards...</div>
      <div v-if="error" class="error-message">Error loading data: {{ error.message || error }}. Please try again later.</div>
      <div v-if="!loading && !error && seasons.length === 0" class="loading">No seasons found</div>
    </div>
  </div>

</template>

<style scoped>
.home-container {
  border: 5px solid red;
  background-color: #eee;
}

#seasons-container {
  margin-top: 600px;
  padding-bottom: 50px;
}
.error-message {
  text-align: center;
  margin: 50px 0;
  color: #ff5555;
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
    ...mapState(['loading', 'error', 'seasons'])
  },
  methods: {
    ...mapActions(['fetchSeasons']),
    navigateToCard(cardUuid) {
      this.$router.push(`/card/${cardUuid}`)
    }
  },
  mounted() {
 this.fetchSeasons();
  },
  // Keep the temporary styles in the style block and template structure
  // We will remove them later once the issue is identified.
};
</script>