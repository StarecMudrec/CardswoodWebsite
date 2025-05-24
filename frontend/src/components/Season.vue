<template>
  <div class="season">
    <div class="season-header">
      <h2 class="season-title">{{ season.name }}</h2>
      <button v-if="selectedCards.length > 0" @click="deleteSelectedCards" class="delete-selected-button">
        DELETE ({{ selectedCards.length }})
      </button>
      <button @click="$router.push('/add-card')" class="add-card-button">
        + Add New Card
      </button>
    </div>
    <div class="cards-container">
      <!-- Pass isSelected prop to Card component -->
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
      // Log the error clearly
      console.error('Error loading cards:', err)
    } finally {
      this.loading = false
    }
  },
  watch: {
    // Watch for changes in selectedCards and update the local cards data
    // to reflect the selection state for each card.
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
      // This method is no longer directly used by individual card clicks
      // but kept in case it's needed elsewhere or for future features.
      try {
        this.loading = true;
        await deleteCard(cardId);
      } catch (err) {
        this.error = err;
        console.error('Error deleting card:', err);
      } finally {
        this.loading = false;
      }
    }
    , // <-- Removed extraneous comma
    handleCardSelected(cardId, isSelected) {
      // Update the selectedCards array based on the event from Card.vue
      if (isSelected) {
        // Add cardId if it's not already in the array
        if (!this.selectedCards.includes(cardId)) {
          this.selectedCards.push(cardId);
        }
      } else {
        this.selectedCards = this.selectedCards.filter(id => id !== cardId);
      }
    },
    async deleteSelectedCards() {
      if (confirm(`Are you sure you want to delete ${this.selectedCards.length} selected cards?`)) {
        try {
          this.loading = true;
          await Promise.all(this.selectedCards.map(cardId => deleteCard(cardId)));
          this.selectedCards = []; // Clear selected cards array after successful deletion
          // Refetch all cards for the season to update the view
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
  background: none; /* Make background transparent */
  color: red; /* Red text color */
  border: none;
  padding: 0; /* Remove padding */
  margin: 0 auto; /* Center the button horizontally */
  display: block; /* Ensure it takes up its own line for centering */
  cursor: pointer;
  transition: opacity 0.3s ease;
  font-family: var(--font-family-main);
  /* Adjust font styles for visibility */
  font-size: 18px; 
  font-weight: bold;
  font-weight: 750;
  font-size: 20px;
  letter-spacing: 0.2px;
}

.delete-selected-button:hover {
  opacity: 1; /* Increase opacity on hover */
}

/* Add text shadow to the delete button */
.delete-selected-button {
  /* Adjust shadow based on desired effect */
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5); 
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
