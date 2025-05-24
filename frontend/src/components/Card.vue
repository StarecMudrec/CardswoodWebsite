<template>
  <div class="card" v-if="card">
    <div class="image-wrapper">
      <img 
        :src="card.img ? `/card_imgs/${card.img}` : '/placeholder.jpg'"
        :alt="card.name"
        class="card-image"
        @error="handleImageError"
      >
    </div>
    <div class="card-content">
      <h3 class="card-title">{{ card.name }}</h3>
      <p class="card-category">{{ card.category }}</p>
    </div>
    <button @click.stop="deleteCard" class="delete-button">
      &#x1F5D1; <!-- Trash bin icon -->
    </button>
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
  methods: {
    handleImageError(e) {
      e.target.src = '/placeholder.jpg'
    },
    deleteCard() {
      this.$emit('card-deleted', this.card.uuid);
    }
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
  transition: transform 0.2s ease;
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

.card-content {
  padding: 16px;
}

.card-title {
  font-size: 1.1rem;
  margin: 0 0 8px;
  color: var(--accent-color);
}

.card-category {
  font-size: 0.9rem;
  color: #888;
  margin: 0;
}

.delete-button {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background-color: rgba(255, 0, 0, 0.7); /* Semi-transparent red */
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
  font-size: 1.1rem;
  line-height: 1;
  opacity: 0; /* Hidden by default */
  transition: opacity 0.2s ease;
  z-index: 10; /* Ensure button is above other card content */
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
