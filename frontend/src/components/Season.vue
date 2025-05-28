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
      <h2 class="season-title">
        <span v-if="!editingSeasonName">{{ season.name }}</span>
        <input
          v-else
          v-model="editableSeasonName"
          @blur="saveSeasonName"
          @keyup.enter="saveSeasonName"
          ref="seasonNameInput"
          class="edit-input"
        >
        <span v-if="isUserAllowed" class="edit-icon" @click="toggleSeasonNameEdit">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </span>
        <!-- Кнопка удаления сезона -->
        <span v-if="isUserAllowed" class="edit-icon delete-season-icon" @click="confirmSeasonDelete">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 6h18"></path>
            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
          </svg>
        </span>
      </h2>
      <button v-if="selectedCards.length > 0" @click="deletingItemType = 'cards'; showDeleteConfirmation = true;" class="delete-selected-button">
        <i class="bi bi-trash"></i> ({{ selectedCards.length }})
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
import { fetchCardsForSeason, deleteCard, checkUserPermission, fetchUserInfo, updateSeason, deleteSeason } from '@/api'
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
      isUserAllowed: false, // Initialize to false
      editingSeasonName: false,
      editableSeasonName: ''
    }
  },
  async created() {
    this.loading = true;
    try {
      this.cards = await fetchCardsForSeason(this.season.uuid);

      console.log('Loaded cards:', this.cards);
      // Fetch user info to get the Telegram username
      const userInfo = await fetchUserInfo();
      const username = userInfo ? userInfo.username : null;

      if (username) {
        const permissionResponse = await checkUserPermission(username);
        this.isUserAllowed = permissionResponse.is_allowed;
        this.$emit('emitUserAllowedStatus', this.isUserAllowed);
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
          isSelected: newSelectedCards.includes(card.uuid)
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
    },
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
      if (this.deletingItemType === 'cards') {
        this.deleteSelectedCards();
      } else if (this.deletingItemType === 'season') {
        this.deleteSeason();
      }
      this.deletingItemType = null; // Сбросить тип удаляемого элемента
    },
    confirmSeasonDelete() {
      this.deletingItemType = 'season';
      this.showDeleteConfirmation = true;
    },
    cancelDelete() {
      this.showDeleteConfirmation = false;
      this.deletingItemType = null; // Сбросить тип удаляемого элемента
    },
    async deleteSeason() {
      try {
        this.loading = true;
        await deleteSeason(this.season.uuid);
        this.$emit('season-deleted', this.season.uuid);
      } catch (err) {
        this.error = err;
        console.error('Error deleting season:', err);
      } finally {
        this.loading = false;
      }
    },
    toggleSeasonNameEdit() {
      if (this.editingSeasonName) {
        this.editingSeasonName = false;
      } else {
        this.editableSeasonName = this.season.name;
        this.editingSeasonName = true;
        this.$nextTick(() => {
          this.$refs.seasonNameInput?.focus();
        });
      }
    },
    async saveSeasonName() {
      if (!this.editableSeasonName || this.editableSeasonName === this.season.name) {
        this.editingSeasonName = false;
        return;
      }

      try {
        this.loading = true;
        const updatedSeason = await updateSeason(this.season.uuid, { name: this.editableSeasonName });
        this.season.name = updatedSeason.name; // Update the local season object's name
        this.season.name = this.editableSeasonName; // Update the local season object's name
        // This line is redundant as the above line already updates the name from the API response.
        // Removing the emit for simplicity if not used by parent, otherwise keep it.
        // this.$emit('season-updated', { ...this.season, name: this.editableSeasonName });

        this.editingSeasonName = false;
      } catch (err) {
        this.error = err;
        console.error('Error updating season name:', err);
      } finally {
        this.loading = false;
      }
    },
  }
}
</script>

<style scoped>
/* Add these new styles */
.season-title {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.edit-icon {
  margin-left: 10px;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
}
.delete-season-icon { 
  color: red;
}

.edit-icon:hover {
  opacity: 1;
  background-color: rgba(255, 255, 255, 0.1);
}

.edit-icon svg {
  width: 16px;
  height: 16px;
}

.edit-input {
  font-size: inherit;
  font-family: inherit;
  color: inherit;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--accent-color);
  border-radius: 4px;
  padding: 5px;
  width: auto;
  max-width: 100%;
  text-align: inherit;
  transition: inherit;
  text-shadow: inherit;
  letter-spacing: inherit;
}

.edit-input:focus {
  border-color: white;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3);
  outline: none;
}

/* Existing styles remain unchanged */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
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
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
  background-color: var(--text-color);
  transition: width 0.3s ease;
}

.cancel-button:hover {
  color: var(--text-color);
}

.cancel-button:hover .button-text::after {
  width: 100%;
}

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
  margin-left: 15px;
}

.delete-selected-button::after {
 content: '';
  position: absolute;
  bottom: 0;
 left: 0;
 width: 0;
 height: 1px;
 background-color: red;
 transition: width 0.3s ease;
}

.delete-selected-button:hover {
  color: red;
 -webkit-text-stroke: 0.15px darkred;
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
  min-height: 80px;
  margin: 15px;
  border: 2px dashed #555;
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
  justify-content: center;
  grid-template-columns: repeat(auto-fit, minmax(220px, 260px));
}

.add-card-button:hover {
  color: var(--hover-color);
}

@media (max-width: 768px) {
 .desktop-only {
    display: none;
 }
 .mobile-only {
    display: flex;
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

@media (min-width: 1600px) {
  .season {
    max-width: 1400px;
  }
}
</style>