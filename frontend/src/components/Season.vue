<template>
  <div class="season">
    <!-- Модальное окно подтверждения удаления -->
    <div v-if="showDeleteConfirmation" class="modal-overlay">
      <div class="modal-content">
        <h3 class="modal-title">Are you sure?</h3>
        <div class="modal-buttons">
          <button @click="confirmDelete" class="delete-button">
            <span class="button-text">Delete</span>
          </button>
          <button @click="cancelDelete" class="cancel-button">
            <span class="button-text">Cancel</span>
          </button>
        </div>
      </div>
    </div>

    <div class="season-header">
      <h2 class="season-title">{{ season.name }}</h2>
      <button v-if="selectedCards.length > 0" @click="showDeleteConfirmation = true" class="delete-selected-button">
        <i class="bi bi-trash"></i> ({{ selectedCards.length }})\
      </button>
      <button v-if="isUserAllowed" @click="$router.push('/add-card')" class="add-card-button desktop-only">
        + Add New Card
      </button>
    </div>
    <div class="cards-container">
      <Card
        v-for="card in cards"
        :key="card.uuid"
        :card="card || {}"
        @card-selected="handleCardSelected"
        @card-clicked="handleCardClicked"
        @delete-card="handleCardDeleted(card.id)"
        :allow-selection="isUserAllowed"
      />
      <div v-if="cards.length === 0" style="grid-column: 1/-1; text-align: center; color: #666;">
        No cards in this season
      </div>
      <div v-if="isUserAllowed" class="add-card-as-card mobile-only" @click="$router.push('/add-card')">
        + Add New Card
      </div>
    </div>
  </div>
</template>

<script>
import Card from './Card.vue'
import { fetchCardsForSeason, deleteCard, checkUserPermission, fetchUserInfo  } from '@/api'
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
      error: null,
      showDeleteConfirmation: false,
      isUserAllowed: false // Initialize to false
    }
  },
  async created() {
    this.loading = true;
    try {
      this.cards = await fetchCardsForSeason(this.season.uuid);

      // Fetch user info to get the Telegram username
      const userInfo = await fetchUserInfo();
      const username = userInfo ? userInfo.username : null;

      console.log(username);
      if (username) {
        const permissionResponse = await checkUserPermission(username);
        this.isUserAllowed = permissionResponse.is_allowed;
      }

    } catch (err) {
      this.error = err;
      console.error('Error loading cards:', err);
    } finally {
      this.loading = false;
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
    handleCardClicked(cardUuid) {
      this.$emit('card-clicked', cardUuid);
    },
    handleCardSelected(cardId, isSelected) {
      if (isSelected) {
        this.selectedCards.push(cardId);
      } else {
        this.selectedCards = this.selectedCards.filter(id => id !== cardId);
      }
    },
    async deleteSelectedCards() {
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
    },
    confirmDelete() {
      this.showDeleteConfirmation = false;
      this.deleteSelectedCards();
    },
    cancelDelete() {
      this.showDeleteConfirmation = false;
    }

  }
}
</script>

<style scoped>
/* Стили модального окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--card-bg);
  padding: 17px;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  border: 1px solid var(--card-bg);
}

.modal-title {
  color: var(--text-color);
  font-weight: 500;
  margin-bottom: 15px;
  margin-top: 15px;
  font-size: 28px;
}

.modal-content p {
  color: white;
  margin-bottom: 20px;
  font-size: 22px;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

/* Стили для кнопки Delete (как в шапке сезона) */
.delete-button {
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  font-size: 22px;
  font-weight: 500;
  padding: 5px 0;
  position: relative;
  text-decoration: none;
  transition: color 0.3s ease;
  font-family: var(--font-family-main);
}

.delete-button .button-text {
  position: relative;
}

.delete-button .button-text::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background-color: red;
  transition: width 0.3s ease;
}

.delete-button:hover {
  color: red;
  -webkit-text-stroke: 0.15px darkred;
}

.delete-button:hover .button-text::after {
  width: 100%;
}

/* Стили для кнопки Cancel (как Back to home в AddCard) */
.cancel-button {
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  font-size: 22px;
  font-weight: 500;
  padding: 5px 0;
  position: relative;
  text-decoration: none;
  transition: color 0.3s ease;
  font-family: var(--font-family-main);
}

.cancel-button .button-text {
  position: relative;
}

.cancel-button .button-text::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background-color: var(--hover-color);
  transition: width 0.3s ease;
}

.cancel-button:hover {
  color: var(--hover-color);
}

.cancel-button:hover .button-text::after {
  width: 100%;
}

/* Адаптивные стили для мобильных устройств */
@media (max-width: 768px) {
  .modal-content {
    padding: 20px;
  }

  .modal-title {
    font-size: 24px;
  }

  .modal-content p {
    font-size: 16px;
  }

  .modal-buttons {
    flex-direction: column;
    gap: 15px;
  }

  .delete-button,
  .cancel-button {
    font-size: 18px;
    padding: 8px 0;
  }
}
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
  background: none;
  border: none;
  color: var(--text-color); /* Use text color for initial state */
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
  margin-left: 15px;
}

.delete-selected-button::after {
 content: '';
  position: absolute;
  bottom: 0;
 left: 0;
 width: 0;
 height: 1px;
 background-color: red; /* Red underline on hover */
 transition: width 0.3s ease;
}

.delete-selected-button:hover {
  color: red; /* Red text on hover */
 -webkit-text-stroke: 0.15px darkred; /* Darker red stroke on hover */
}

.delete-selected-button:hover::after {
 width: 100%;
}


.add-card-as-card {
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
  color: var(--text-color);
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s ease;
  min-height: 80px; /* Adjust height as needed */
  margin: 15px; /* Match card margin */
  border: 2px dashed #555; /* Dashed border to indicate it\'s an interactive area */
}

.add-card-as-card:hover {
 transform: translateY(-5px);
 border-color: var(--accent-color);
 color: var(--accent-color);
}

.desktop-only {
  display: block;
}
.mobile-only {
  display: none;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0px;
  /* 🟡 ЦЕНТРИРОВАНИЕ НА ДЕСКТОПЕ */
  justify-content: center;
  grid-template-columns: repeat(auto-fit, minmax(220px, 260px));
}

/* Можно добавить hover-эффект для цвета текста, как в Navbar */
.add-card-button:hover {
  color: var(--hover-color);
}

@media (max-width: 768px) {
 .desktop-only {
    display: none;
 }
 .mobile-only {
    display: flex; /* Show as flex to center content */
 }
}

@media (max-width: 768px) {
  .cards-container {
    grid-template-columns: repeat(1, 1fr);
    gap: 10px;
    padding: 0 10px;
  }
 .card {
  margin: 0;
 }
}
/* 🟡 УБИРАЕМ РАСТЯГИВАНИЕ НА ОГРОМНЫХ ЭКРАНАХ */
@media (min-width: 1600px) {
  .season {
    max-width: 1400px;
  }
}
</style>