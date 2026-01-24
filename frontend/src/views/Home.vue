<template>
  <div class="page-container">
    <div class="background-container" aria-hidden="true"></div>
    <header class="page-header">
      <img src="/logo_noph.png" alt="Логотип" class="background-logo">
      <hr class="separator-line">
    </header>

    <main class="content-wrapper">
      <section id="seasons-container" class="seasons-section" aria-labelledby="seasons-title">
        <h1 id="seasons-title" class="visually-hidden">Сезоны</h1>
        <div v-if="loading" class="loading">Загрузка карточек...</div>
        <div v-else-if="error" class="error-message" role="alert">
          Ошибка загрузки данных: {{ error.message || error }}. Пожалуйста, попробуйте позже.
        </div>
        <div v-else-if="seasons.length === 0" class="loading">Сезоны не найдены</div>
        <Season
          v-for="season in seasons"
          :key="season.uuid"
          :season="season"
          @card-clicked="navigateToCard"
          @add-card="navigateToAddCard"
          @emitUserAllowedStatus="updateUserAllowedStatus"
          @season-deleted="handleSeasonDeleted"
        />
      </section>

      <div v-if="isUserAllowed" class="add-season-footer">
        <div class="add-new-season-btn" @click="navigateToAddSeason">
          + Добавить сезон
        </div>
      </div>
    </main>

    <footer class="page-footer">
      <Footer />
    </footer>
  </div>

</template>

<style scoped>
.page-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-header {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
}

.content-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 1;
  z-index: 2;
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
  z-index: 2; /* Ensure it's behind the content */
}

.separator-line {
  position: relative;
  margin-top: 47vh;
  height: 2px;
  background-color: white;
  border: none;
  z-index: 2;
  width: 75%;
}

#seasons-container {
  position: relative; /* Essential for z-index to work correctly relative to the background */
  margin-top: 30px; /* Push content down by the height of the background */
  flex: 1;
}

.seasons-section {
  z-index: 2;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
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

.page-footer {
  position: relative;
  z-index: 2;
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
    },
    // Add a new method to handle season deletion
    handleSeasonDeleted(deletedSeasonUuid) {
      // Call the mutation to remove the season from the VueX store
      this.REMOVE_SEASON(deletedSeasonUuid);
    }
  },
  mounted() {
    this.fetchSeasons()
  }
}
</script>