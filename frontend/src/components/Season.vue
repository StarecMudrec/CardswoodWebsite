<template>
  <div class="season">
    <h2 class="season-title">{{ season.name }}</h2>
    <button @click="$router.push('/add-card')" class="add-card-button">
      Add New Card
    </button>
    <div class="cards-container">
      <Card 
        v-for="card in cards" 
        :key="card.uuid" 
	:card="card || {}"
        @click="$emit('card-clicked', card.uuid)"
      />
      <div v-if="cards.length === 0" style="grid-column: 1/-1; text-align: center; color: #666;">
        No cards in this season
      </div>
    </div>
  </div>
</template>

<script>
import Card from './Card.vue'
import { fetchCardsForSeason } from '@/api'

export default {
  components: {
    Card
  },
  props: {
    season: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      cards: [],
      loading: false,
      error: null
    }
  },
  async created() {
    this.loading = true
    try {
      this.cards = await fetchCardsForSeason(this.season.uuid)
    } catch (err) {
      this.error = err
      console.error('Error loading cards:', err)
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.season {
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 25px;
  margin-bottom: 40px;
  border: 1px solid #333;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.season-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}

.season-title {
  font-size: 24px;
  margin: 0;
  color: var(--accent-color);
  font-weight: 500;
  padding-bottom: 10px;
  border-bottom: 1px solid #333;
  flex-grow: 1;
}

.add-card-button {
  background: none;
  border: none;
  color: var(--accent-color);
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 1px;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
  padding: 5px 0;
  margin-left: 20px;
  position: relative;
  text-decoration: none;
  transition: color 0.3s ease;
}

.add-card-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: var(--hover-color);
  transition: width 0.3s ease;
}

.add-card-button:hover {
  color: var(--hover-color);
  -webkit-text-stroke: 0.15px var(--hover-border-color);
}

.add-card-button:hover::after {
  width: 100%;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0px;
}

@media (min-width: 1024px) {
  .cards-container {
    justify-content: center;
    grid-template-columns: repeat(auto-fit, minmax(220px, 260px));
  }
}

@media (max-width: 768px) {
  .cards-container {
    gap: 20px;
    padding: 15px 0;
  }
  
  .season-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .add-card-button {
    margin: 10px 0 0 0;
    align-self: flex-end;
  }
}

@media (min-width: 1600px) {
  .season {
    max-width: 1400px;
  }
}
</style>
