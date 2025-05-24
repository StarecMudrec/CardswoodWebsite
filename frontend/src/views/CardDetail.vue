<template>
  <div>
    <div class="background-container"></div>
    <div class="card-detail-container">
      <div v-if="loading" class="loading">Loading card details...</div>
      <div v-else-if="error" class="error-message">Error loading card: {{ error }}</div>
      <div v-else class="card-detail">
        <div class="card-image-container">
          <img 
            v-if="card.img && !imageError" 
            :src="`/card_imgs/${card.img}`" 
            :alt="card.name" 
            class="card-detail-image"
            @error="imageError = true"
          />
          <div v-else class="image-placeholder">No image available</div>
        </div>
        
        <div class="card-content-wrapper">
          <!-- Название карточки и главная разделительная линия -->
          <div class="card-header-section">
            <div class="title-container">
              <div class="editable-field">
                <h1 v-if="!editingName" ref="cardNameRef">{{ card.name }}</h1>
                <input v-else type="text" v-model="editedName"
                  @blur="saveName" @keyup.enter="saveName" @keyup.esc="cancelEditingName">
                <span v-if="!editingName" class="edit-icon" @click="startEditingName">Edit</span>
                <input v-else type="text" v-model="editedName">
                <span class="edit-icon" @click="startEditingName">Edit</span>
                <button v-if="editingName" @click="saveName">Save</button>
                <button v-if="editingName" @click="cancelEditingName">Cancel</button>
              </div>
            </div>
            <div class="main-divider"></div>
          </div>
          
          <!-- Описание карточки -->
          <div class="card-description-section">
            <div class="card-description editable-field">
              <p v-if="!editingDescription">{{ card.description }}</p>
              <textarea v-else v-model="editedDescription"
                @blur="saveDescription" @keyup.enter="saveDescription" @keyup.esc="cancelEditingDescription"></textarea>

              <span v-if="!editingDescription" class="edit-icon" @click="startEditingDescription">Edit</span>
              <!-- Buttons can be added here if needed, but blur/enter save is common for textareas -->
              <!-- <button v-if="editingDescription" @click="saveDescription">Save</button> -->
              <button v-if="editingDescription" @click="cancelEditingDescription">Cancel</button>

            </div>
            <div class="secondary-divider"></div>
          </div>
          
          <!-- Информация о категории и сезоне -->
          <div class="card-info-section">
            <div class="card-info-columns">
              <div class="card-info-column">
                <h3>Category:</h3>
                <div class="editable-field">
                  <p v-if="!editingCategory">{{ card.category }}</p>
                  <input v-else type="text" v-model="editedCategory">

                  <span v-if="!editingCategory" class="edit-icon" @click="startEditingCategory">Edit</span>
                  <span class="edit-icon" @click="startEditingCategory">Edit</span>
                  <button v-if="editingCategory" @click="saveCategory">Save</button>
                  <button v-if="editingCategory" @click="cancelEditingCategory">Cancel</button>
                </div>

              </div>
              <div class="card-info-column">
                <h3>Rarity:</h3>
                <div class="editable-field">
                  <p v-if="!editingRarity">{{ card.rarity }}</p>
                  <input v-else type="text" v-model="editedRarity">
                  <span class="edit-icon" @click="startEditingRarity">Edit</span>
                  <span v-if="!editingRarity" class="edit-icon" @click="startEditingRarity">Edit</span>

                  <button v-if="editingRarity" @click="saveRarity">Save</button>
                  <button v-if="editingRarity" @click="cancelEditingRarity">Cancel</button>
                </div>
                <h3>Season:</h3>
                <p>{{ seasonName }}</p>
              </div>
            </div>
          </div>
          
          <!-- Комментарии -->
          <div class="comments-section">
            <div v-if="comments.length === 0" class="no-comments">
              No comments yet
            </div>
            <div v-else class="comments-list">
              <div v-for="comment in comments" :key="comment.id" class="comment">
                <div class="comment-text">{{ comment.text }}</div>
                <div class="comment-meta">User #{{ comment.user_id }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchCardInfo, fetchSeasonInfo, fetchComments, updateCard } from '@/api'
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'

export default {
  props: {
    uuid: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const card = ref({})
    const seasonName = ref('')
    const comments = ref([])
    const loading = ref(true)
    const error = ref(null)
    const imageError = ref(false)
    const cardNameRef = ref(null)

    // Editing state variables
    const editingName = ref(false)
    const editingDescription = ref(false)
    const editingCategory = ref(false)
    const editingRarity = ref(false)

    // Edited value variables
    const editedName = ref('')
    const editedDescription = ref('')
    const isMobile = ref(false)

    const adjustFontSize = () => {
      nextTick(() => {
        if (!cardNameRef.value) return;
        
        const element = cardNameRef.value;
        const container = element.parentElement;
        
        element.style.fontSize = '';
        element.style.whiteSpace = 'nowrap';
        
        const containerWidth = container.clientWidth;
        let fontSize = 100;
        element.style.fontSize = `${fontSize}px`;
        void element.offsetWidth;
        
        if (element.scrollWidth > containerWidth) {
          const ratio = containerWidth / element.scrollWidth;
          fontSize = Math.max(
            28, // Минимальный размер
            Math.min( // Не уменьшаем резко
              fontSize, 
              Math.floor(fontSize * ratio * 0.85) // Сохраняем 15% запаса
            )
          );
          element.style.fontSize = `${fontSize}px`;
          
          // Если после мягкого уменьшения всё ещё не влезает - переносим
          if (element.scrollWidth > containerWidth * 1.05) {
            element.style.whiteSpace = 'normal';
            element.style.lineHeight = '1.2';
          }
        }
      });
    };

    const loadData = async () => {
      try {
        loading.value = true
        card.value = await fetchCardInfo(props.uuid)
        
        const season = await fetchSeasonInfo(card.value.season_id)
        seasonName.value = season.name
        
        comments.value = await fetchComments(card.value.id)

        editedName.value = card.value.name;
        editedDescription.value = card.value.description;
        // Initialize other edited fields as needed
        
        // Вызываем после полного рендеринга
        setTimeout(adjustFontSize, 0)
      } catch (err) {
        error.value = err.message || 'Failed to load card details'
        console.error('Error loading card:', err)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      window.addEventListener('resize', adjustFontSize)
      loadData()
    })

    onUnmounted(() => {
      window.removeEventListener('resize', adjustFontSize)
    })

    watch(() => props.uuid, loadData)

    // Editing functions
    const startEditingName = () => {
      editedName.value = card.value.name;
      editingName.value = true;
       nextTick(() => { // Focus the input after it becomes visible
         // Assuming the input is a direct sibling or child you can reference
         // A more robust way might be to use template refs
         document.querySelector('.title-container input[type="text"]')?.focus();
       });
    };
    const saveName = async () => {
      if (editedName.value !== card.value.name) {
        try {
          // Assuming updateCard expects an object with the field to update
          await updateCard(card.value.uuid, { name: editedName.value });
          card.value.name = editedName.value; // Update local state
        } catch (err) {
          console.error('Error saving name:', err);
          // Optionally display an error message to the user
        }
      }
      editingName.value = false;
      // Re-adjust font size after saving
      nextTick(adjustFontSize);
    };
    const cancelEditingName = () => {
      editingName.value = false;
       // Re-adjust font size after cancelling
      nextTick(adjustFontSize);
    };

    const startEditingDescription = () => {
      editedDescription.value = card.value.description;
      editingDescription.value = true;
       nextTick(() => {
         document.querySelector('.card-description-section textarea')?.focus();
       });
    };
    const saveDescription = async () => {
      if (editedDescription.value !== card.value.description) {
        try {
          await updateCard(card.value.uuid, { description: editedDescription.value });
          card.value.description = editedDescription.value; // Update local state
        } catch (err) {
          console.error('Error saving description:', err);
        }
      }
      editingDescription.value = false;
    };
    const cancelEditingDescription = () => {
      editingDescription.value = false;
    };

    const startEditingCategory = () => {
      editedCategory.value = card.value.category;
      editingCategory.value = true;
    };
    const saveCategory = async () => {
       if (editedCategory.value !== card.value.category) {
        try {
          await updateCard(card.value.uuid, { category: editedCategory.value });
          card.value.category = editedCategory.value; // Update local state
        } catch (err) {
          console.error('Error saving category:', err);
        }
      }
      editingCategory.value = false;
    };
    const cancelEditingCategory = () => {
      editingCategory.value = false;
    };

    const startEditingRarity = () => {
      editedRarity.value = card.value.rarity;
      editingRarity.value = true;
    };
    const saveRarity = async () => {
      // Similar save logic for rarity
      editingRarity.value = false;
    };
    const cancelEditingRarity = () => {
      editingRarity.value = false;
    };

    return {
      card,
      seasonName,
      comments,
      loading,
      error,
      imageError: imageError,\
      cardNameRef
      ,\n\n      // Editing state and values\n      editingName,\n      editingDescription,\n      editingCategory,\n      editingRarity,\n      editedName,\n      editedDescription,\n      editedCategory,\n      editedRarity,\n\n      // Editing functions\n      startEditingName,\n      saveName,\n      cancelEditingName,\n      startEditingDescription,\n      saveDescription,\n      cancelEditingDescription,\n      startEditingCategory,\n      saveCategory,\n      cancelEditingCategory,\n      startEditingRarity,\n      saveRarity,\n      cancelEditingRarity\n
    }
  }
}
</script>

<style scoped>
.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%;
  z-index: -1;
}

.card-detail-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px;
}

.card-detail {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 40px;
  margin-top: 30px;
}

.card-image-container {
  position: relative;
}

.card-detail-image {
  width: 100%;
  max-height: 600px;
  object-fit: contain;
  border-radius: 17px;
  border: 10px solid var(--bg-color);
  background-color: #1e1e1e;
}

.image-placeholder {
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1e1e1e;
  color: #666;
  border-radius: 17px;
  border: 10px solid var(--bg-color);
}

.card-content-wrapper {
  display: flex;
  flex-direction: column;
}

/* Исправленная секция заголовка */
.card-header-section {
  /* Keep existing styles */
  margin-top: 64px; /* Add top margin to push content down (adjust value as needed) */
  /* Add other styling for spacing or alignment */
  position: relative;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.title-container {
  position: absolute;
  bottom: 17px; /* Расстояние до разделителя */
  width: 100%;
}

.card-header-section h1 {
  margin: 0;
  padding: 0;
  white-space: nowrap;
  font-size: 100px;
  line-height: 1;
  color: var(--text-color);
  display: inline-block;
  vertical-align: bottom;
  transform-origin: left bottom;
  transition: font-size 0.2s ease;
  transition: color 0.3s ease, box-shadow 0.3s ease; /* Add box-shadow to transition */
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Semi-transparent dark shadow */
}

.main-divider {
  height: 2px;
  width: 100%;
  background-color: var(--card-border-color);
  top: 20%;
  position: relative;
  bottom: -20px; /* Позиционируем ниже текста */
}

/* Остальные стили без изменений */
.card-description-section {
  padding: 30px 0;
}

.card-description {
  font-size: 18px;
  line-height: 1.6;
  color: var(--text-color);
  text-align: center; 
}

.secondary-divider {
  height: 1px;
  width: 100%;
  background-color: var(--card-border-color);
  margin-top: 30px;
}

.card-info-section {
  padding: /*2*/0px 0;
}

.card-info-columns {
  display: flex;
  justify-content: space-around;
}

.card-info-column {
  flex: 1;
  text-align: center;
}

.card-info-column h3 {
  font-size: 25px;
  margin-bottom: 10px;
  color: var(--accent-color);
}

.card-info-column p {
  font-size: 20px;
  line-height: 1.6;
  color: var(--text-color);
}

.comments-section {
  margin-top: auto;
  padding-top: 40px;
  text-align: center;
}

.no-comments {
  color: #666;
  font-style: italic;
}

.comments-list {
  max-width: 800px;
  margin: 0 auto;
}

.comment {
  background-color: #1e1e1e;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  text-align: left;
}

.comment-text {
  margin-bottom: 8px;
  color: var(--text-color);
}

.comment-meta {
  font-size: 14px;
  color: #aaa;
}

@media (max-width: 768px) {
  .card-detail {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .card-header-section {
    text-align: center;
    margin-top: -10px;
    min-height: 57px;
  }

  .card-content-wrapper {
    padding: 0 15px;
  }
  .title-container {
    width: 100%;
    overflow: hidden;
    position: relative;
    bottom: auto;
  }

  .card-header-section h1 {
    font-size: 100px; /* Начальный размер */
    line-height: 1.1;
    margin: 0;
    padding: 0;
    white-space: nowrap;
    transition: all 0.3s ease;
    word-break: break-word;
  }
  .card-header-section h1.force-wrap {
    white-space: normal;
    line-height: 1.3;
  }

  .main-divider {
    margin-top: 15px;
  }
  .card-description {
    position: relative;
    left: -5%;
    width: 110%;
  }

  .card-detail-image {
    border-radius: 15px;
    border: 10px solid var(--bg-color);
  }
}
</style>