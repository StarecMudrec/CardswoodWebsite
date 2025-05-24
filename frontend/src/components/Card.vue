<template>
  <div
    class="card"
    :class="{ 'selected': isSelected }"
    v-if="card"@click="handleCardClick"
  >
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
    <input
      type="checkbox"
      class="selection-checkbox"
      :checked="isSelected"
      @change="handleCheckboxChange"
      @click.stop
    >

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
      isSelected: false,
 };
  },
  methods: {
    handleImageError(e) {
      e.target.src = '/placeholder.jpg';
    },
    handleCardClick(event) {
      // Prevent triggering on checkbox click
      if (event.target.classList.contains('selection-checkbox')) {
        return;
      }
      // Navigate on any click unless it's the checkbox
      // This handler is primarily for desktop, mobile is handled by handleCardContentClick
      this.$emit('card-clicked', this.card.uuid);
    },
    handleCheckboxChange(event) {
      this.isSelected = event.target.checked;
      this.$emit('card-selected', this.card.uuid, this.isSelected);
    },

    toggleSelection() {
      this.isSelected = !this.isSelected; // Toggle selection mapState
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
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Use consistent shadow */
  position: relative; /* Added for absolute positioning of the button */
  transition: transform 0.2s ease, border 0.2s ease;
  margin: 15px;
}

.card:hover {
  transform: translateY(-5px);
}

/* Style for the selection checkbox */
.selection-checkbox {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 1; /* Ensure it's above the image */
  width: 20px;
  height: 20px;
  cursor: pointer;
  /* Hide on mobile by default */
  display: none;
}

/* Show on desktop */
@media (min-width: 769px) { /* Adjust breakpoint as needed */
  .selection-checkbox {
    display: block;
  }
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
  transition: filter 0.3s ease; /* Add transition for blur */
}

.card.selected {
  border: 4px solid rgba(255, 42, 42, 0.32);
}
.card.selected::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 42, 42, 0.24);
  z-index: 0; /* Lower than checkbox and potential future delete button */
  filter: blur(4px);
}
.card.selected .card-inner-content {
  filter: blur(4px) opacity(0.5);
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

    .selection-checkbox {
      display: block; /* Ensure checkbox is visible on mobile */
    }
  }

  .image-wrapper {
    height: calc(var(--card-width) * 1.4);
  }
}

@media (max-width: 480px) {
  .card {
    --card-width: 90vw;
    margin: 8px auto;

    .selection-checkbox {
      display: block; /* Ensure checkbox is visible on mobile */
      width: 30px;
      height: 30px;
    }
  }
}
</style>
