<template>
  <div class="card" :class="{ 'selected': isSelected }" v-if="card" @click="toggleSelection">
    <div class="card-inner-content">
      <div class="image-wrapper">
        <img
          :src="card.img ? `/card_imgs/${card.img}` : '/placeholder.jpg'"
          :alt="card.name"
          class="card-image"
          @error="handleImageError"
        >
      </div>
      <div class="card-content">
        <div class="card-info">
          <h3 class="card-title">{{ card.name }}</h3>
          <span class="card-rarity">{{ card.rarity }}</span>
        </div>
        <div class="card-meta">
          <p class="card-category">{{ card.category }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    card: {
      type: Object,
      required: true,
      validator: card => 'name' in card && 'img' in card
    }
  },
  data() {
    return {
      isSelected: false
    };
  },
  methods: {
    handleImageError(e) {
      e.target.src = '/placeholder.jpg';
    },
    toggleSelection() {
      this.isSelected = !this.isSelected;
      this.$emit('card-selected', this.card.id, this.isSelected);
    },
    deleteCard() {
      this.$emit('delete-card', this.card.id);
    },
  }
}
</script>

<style scoped>
.card {
  --card-width: 220px;
  width: var(--card-width);
  background: var(--card-bg);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative; /* Added for absolute positioning of the button */
  transition: transform 0.2s ease, border 0.2s ease;
  margin: 15px;
}

.card:hover {
  transform: translateY(-5px);
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: calc(var(--card-width) * 1.3);
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.card-inner-content {
  transition: filter 0.2s ease; /* Add transition for blur */
}

.card.selected {
  border: 2px solid var(--accent-color);
}
.card.selected .card-inner-content {
  filter: blur(2px);
}
.card-content {
  padding: 16px;
}

.card-info {
  display: flex;
}
.card-category {
  font-size: 0.9rem;
  color: #888;
  margin: 0;
}


/* New styles for card info layout */
.card-info {
 display: flex;
 justify-content: space-between;
 align-items: center;
 margin-bottom: 8px;
}

.card-title {
 font-size: 1.1rem;
 margin: 0;
 color: var(--accent-color);
}

.card-rarity {
  font-size: 0.9rem;
  color: #888;
}
/* 🟡 НОВЫЕ СТИЛИ ДЛЯ КОМПАКТНОГО ВИДА */
.card.compact {
  --card-width: 180px;
  margin: 8px;
  
  .card-content {
    padding: 8px;
  }
  
  .card-title {
    font-size: 0.9rem;
    margin-right: 8px; /* Add spacing between title and rarity in compact view */
  }
}

@media (max-width: 768px) {
  .card {
    --card-width: 48vw;
    margin: 8px 4px;
  }

  .image-wrapper {
    height: calc(var(--card-width) * 1.4);
  }
}

@media (max-width: 480px) {
  .card {
    --card-width: 90vw;
    margin: 8px auto;
  }
}
</style>
