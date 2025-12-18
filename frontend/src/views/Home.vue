<template>
  <div class="page-container page-with-navbar">
    <div class="background-container"></div>
    <img src="/logo_noph.png" alt="Логотип" class="background-logo">
    <hr class="separator-line">

    <div class="content-wrapper">
      <div id="seasons-container">
        <div v-if="loading" class="loading">Загрузка карточек...</div>
        <div v-else-if="error" class="error-message">Ошибка загрузки данных: {{ error.message || error }}. Пожалуйста, попробуйте позже.</div>
        <div v-else-if="seasons.length === 0" class="loading">Сезоны не найдены</div>
        <Season 
          v-for="season in seasons" 
          :key="season.uuid" 
          :season="season" 
          @card-clicked="navigateToCard" deprecated
          @add-card="navigateToAddCard"
          @emitUserAllowedStatus="updateUserAllowedStatus"
          @season-deleted="handleSeasonDeleted"
        />
      </div>

      <div v-if="isUserAllowed" class="add-season-footer">
        <div class="add-new-season-btn" @click="navigateToAddSeason">
          + Добавить сезон
        </div>
      </div>

      <Footer />
    </div>
  </div>

</template>

<style scoped>
.page-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px; /* Adjust height as needed */
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%; /* Position the vertical center 80% down from the top, center horizontally */
  z-index: 1; /* Ensure it's behind the content */
}

.background-logo {
  position: absolute;
  top: 100px;
  left: 50%;
  transform: translate(-50%, 0);
  max-width: 250px; /* Adjust size as needed */
  max-height: 250px; /* Adjust size as needed */
  z-index: 1; /* Ensure it's behind the content */
}

.separator-line {
  position: relative;
  margin-top: 430px; /* Adjust to be below the background image */
  height: 2px;
  background-color: white;
  border: none;
  z-index: 2; /* Ensure it's above the background */
  width: 75%;
}

#seasons-container {
  position: relative; /* Essential for z-index to work correctly relative to the background */
  margin-top: 30px; /* Push content down by the height of the background */
  z-index: 2; /* Ensure content is above the background */
  flex: 1;
}
.error-message {
  text-align: center;
  margin: 50px 0;
  color: #ff5555; /* Red color for errors */
}

.add-season-footer {
  padding: 20px 0 50px;
  text-align: center;
}
.add-new-season-btn {
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: inline-flex;
  justify-content: center;
  align-items: center;
  color: var(--text-color);
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 60px;
  padding: 0 30px;
  border: 2px dashed #555;
  margin: 0 auto;
}

.add-new-season-btn:hover {
  transform: translateY(-5px);
  border-color: var(--accent-color);
  color: var(--accent-color);
}

</style>

<script>
import Season from '@/components/Season.vue'
import Footer from '@/components/Footer.vue'
import { mapActions, mapState, mapMutations } from 'vuex' // Import mapMutations

export default {
  components: {
    Season,
    Footer
  },
  computed: {
    ...mapState(['seasons', 'loading', 'error'])
  },
  data() {
    return {
      isUserAllowed: false
    };
  },
  methods: {
    ...mapActions(['fetchSeasons']),
    ...mapMutations(['REMOVE_SEASON']), // Add mapMutations
    navigateToCard(cardId) { // Deprecated - use @card-clicked on card component directly
      this.$router.push(`/card/${cardId}`);
    },
    updateUserAllowedStatus(isAllowed) {
      console.log('Received user allowed status:', isAllowed);
      this.isUserAllowed = isAllowed;
    },
    navigateToAddCard() {
      // Реализуйте навигацию к странице добавления карточки
      // this.$router.push('/add-card'); // This method seems unused based on template. Leaving as comment.
    },
    async navigateToAddSeason() {
      try {
        // Assuming createSeason is imported from your api file
        const { createSeason } = await import('@/api'); // Import dynamically if not already imported
        const newSeason = await createSeason();
        console.log('New season created:', newSeason);
        await this.fetchSeasons(); // Refresh the list of seasons
        // Removed automatic navigation after season creation
        // this.$router.push(`/season/${newSeason.uuid}`); // Navigate to the new season's page
      } catch (error) {
        console.error('Ошибка создания сезона:', error);
        alert('Не удалось создать сезон.'); // Provide user feedback
      }
    }
    ,
    // Add a new method to handle season deletion
    handleSeasonDeleted(deletedSeasonUuid) {
      // Call the mutation to remove the season from the VueX store
      this.REMOVE_SEASON(deletedSeasonUuid);
    }
  },
  mounted() {
    this.fetchSeasons()
  },
  // Add a new method to handle season deletion
  handleSeasonDeleted(deletedSeasonUuid) {
    // Call the mutation to remove the season from the VueX store
    this.REMOVE_SEASON(deletedSeasonUuid);
  }
}
</script>