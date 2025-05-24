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
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  text-align: center;
  box-shadow: 0 5px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  position: relative; /* Добавляем для позиционирования псевдоэлемента */
  text-decoration: none; /* Убираем стандартное подчеркивание */
}

.add-card-button::after {
  content: '';
  position: absolute;
  bottom: 5px; /* Регулируем расстояние от текста */
  left: 20px; /* Совпадает с padding-left кнопки */
  width: calc(100% - 40px); /* Учитываем padding кнопки */
  height: 1px;
  background-color: transparent;
  transition: background-color 0.3s ease;
}

.add-card-button:hover::after {
  background-color: var(--hover-color); /* Используем тот же цвет, что и в Navbar */
}

/* Можно добавить hover-эффект для цвета текста, как в Navbar */
.add-card-button:hover {
  color: var(--hover-color);
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
