<template>
  <div>
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