<template>
  <div class="season">
    <div class="season-header">
      <h2 class="season-title">{{ season.name }}</h2>
      <button v-if="selectedCards.length > 0" @click="deleteSelectedCards" class="delete-selected-button">
        Delete Selected ({{ selectedCards.length }})
      </button>
      <button @click="$router.push('/add-card')" class="add-card-button">
        + Add New Card
      </button>
    </div>
    <div class="cards-container">
      <Card 
        v-for="card in cards" 
        :key="card.uuid" 
        :card="card || {}"
        @card-selected="handleCardSelected"
        @delete-card="handleCardDeleted(card.uuid)"
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
import { deleteCard } from '@/api'
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
      selectedCards: [],
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
  },
  watch: {
    // Watch for changes in selectedCards and update cards data with selection state
    selectedCards: {
      handler(newSelectedCards) {
        this.cards = this.cards.map(card => ({
          ...card,
          isSelected: newSelectedCards.includes(card.id)
        }));
      },
      deep: true // Watch for changes inside the array
    }
  },
  methods: {
    async handleCardDeleted(cardId) {
      try {
        this.loading = true;
        await deleteCard(cardId);
        // Refetch cards after successful deletion
        this.cards = await fetchCardsForSeason(this.season.uuid);
      } catch (err) {
        this.error = err;
        console.error('Error deleting card:', err);
      } finally {
        this.loading = false;
      }
    }
    ,
    handleCardSelected(cardId, isSelected) {
      if (isSelected) {
        this.selectedCards.push(cardId);
      } else {
        this.selectedCards = this.selectedCards.filter(id => id !== cardId);
      }
    },
    async deleteSelectedCards() {
      if (confirm(`Are you sure you want to delete ${this.selectedCards.length} selected cards?`)) {
        try {
          this.loading = true;
          await Promise.all(this.selectedCards.map(cardId => deleteCard(cardId)));
          this.selectedCards = []; // Clear selected cards
          this.cards = await fetchCardsForSeason(this.season.uuid); // Refetch cards
        } catch (err) {
          this.error = err;
          console.error('Error deleting selected cards:', err);
        } finally {
          this.loading = false;
        }
      }
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
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
}

.season-title {
  font-size: 24px;
  margin: 0;
  color: var(--accent-color);
  font-weight: 500;
}

.add-card-button {
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 1px;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
  padding: 5px 0;
  position: relative;
  text-decoration: none;
  transition: color 0.3s ease;
  white-space: nowrap;
  font-family: var(--font-family-main);
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

.delete-selected-button {
  background-color: rgba(255, 42, 42, 0);
  color: red;
  border: none;
  border-radius: 14px;
  opacity: 0.7;
  cursor: pointer;
  font-size: 1rem;
  transition: opacity 0.3s ease;
  margin-left: 15px;
  font-family: var(--font-family-main);
  font-weight: 750;
  font-size: 20px;
  letter-spacing: 0.2px;
  transition: color 0.3s ease, box-shadow 0.3s ease; /* Add box-shadow to transition */
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Semi-transparent dark shadow */
}

.delete-selected-button:hover {
  /*background-color: rgba(255, 42, 42, 0.32);*/
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
