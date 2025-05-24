<template>
  <div class="season">
    <h2 class="season-title">{{ season.name }}</h2>
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
      <button @click="$router.push('/add-card')" class="add-card-button">
        Add New Card
      </button>
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
  
   /* 🟡 НОВЫЕ СТИЛИ ДЛЯ ЦЕНТРИРОВАНИЯ */
  max-width: 1200px; /* Ограничиваем ширину плашки */
  margin-left: auto;
  margin-right: auto;
}

.season-title {
  font-size: 24px;
  margin-bottom: 20px;
  margin-top: 0px;  
  color: var(--accent-color);
  font-weight: 500;
  padding-bottom: 10px;
  border-bottom: 1px solid #333;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0px;
  /* 🟡 ЦЕНТРИРОВАНИЕ НА ДЕСКТОПЕ */
  @media (min-width: 1024px) {
    justify-content: center;
    grid-template-columns: repeat(auto-fit, minmax(220px, 260px));
  }
}
.add-card-button {
  grid-column: 1/-1; /* Make the button span across all columns */
  margin-top: 20px;
  padding: 10px 20px;
  background-color: var(--card-bg);
  color: var(--accent-color);
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  text-align: center;
  box-shadow: 0 5px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  text-decoration: none;
  letter-spacing: 1px;
}

.add-card-button:hover {
  color: var(--hover-color);
  -webkit-text-stroke: 0.15px var(--hover-border-color);
  transition: color 0.3s ease, box-shadow 0.3s ease; /* Add box-shadow to transition */
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Semi-transparent dark shadow */
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

.add-card-button:hover::after {
  width: 100%;
}

@media (max-width: 768px) {
  .cards-container {
    gap: 20px;        /* Сохраняем адекватное расстояние на мобилках */
    padding: 15px 0;  /* Уменьшаем отступы для маленьких экранов */
  }
}
/* 🟡 УБИРАЕМ РАСТЯГИВАНИЕ НА ОГРОМНЫХ ЭКРАНАХ */
@media (min-width: 1600px) {
  .season {
    max-width: 1400px;
  }
}
</style>
