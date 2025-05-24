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
              <h1 ref="cardNameRef">
                <span v-if="!editing.name">{{ card.name }}</span>
                <input 
                  v-else
                  v-model="editableCard.name"
                  @blur="saveField('name')"
                  @keyup.enter="saveField('name')"
                  @keyup.esc="cancelEditing('name')"
                  ref="nameInput"
                  class="edit-input"
                >
                <span class="edit-icon" @click="toggleEditing('name')">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </span>
              </h1>
            </div>
            <div class="main-divider"></div>
          </div>
          
          <!-- Описание карточки -->
          <div class="card-description-section">
            <div class="card-description">
              <p v-if="!editing.description">{{ card.description }}</p>
              <textarea
                v-else
                v-model="editableCard.description"
                @blur="saveField('description')"
                @keyup.enter="saveField('description')"
                @keyup.esc="cancelEditing('description')"
                ref="descriptionInput"
                class="edit-textarea"
              ></textarea>
              <span class="edit-icon" @click="toggleEditing('description')">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
              </span>
            </div>
            <div class="secondary-divider"></div>
          </div>
          
          <!-- Информация о категории и сезоне -->
          <div class="card-info-section">
            <div class="card-info-columns">
              <div class="card-info-column">
                <h3>
                  Category:
                  <span class="edit-icon" @click="toggleEditing('category')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </span>
                </h3>
                <p v-if="!editing.category" class="category-text">{{ card.category }}</p>
                <input
                  v-else
                  v-model="editableCard.category"
                  @blur="saveField('category')"
                  @keyup.enter="saveField('category')"
                  @keyup.esc="cancelEditing('category')"
                  ref="categoryInput"
                  class="category-input"
                >
              </div>
              <div class="card-info-column">
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
import { fetchCardInfo, fetchSeasonInfo, fetchComments } from '@/api'
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
    const editableCard = ref({})
    const seasonName = ref('')
    const comments = ref([])
    const loading = ref(true)
    const error = ref(null)
    const imageError = ref(false)
    const cardNameRef = ref(null)
    const editing = ref({
      name: false,
      description: false,
      category: false
    })
    const nameInput = ref(null)
    const descriptionInput = ref(null)
    const categoryInput = ref(null)

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
            28,
            Math.min(
              fontSize, 
              Math.floor(fontSize * ratio * 0.85)
            )
          );
          element.style.fontSize = `${fontSize}px`;
          
          if (element.scrollWidth > containerWidth * 1.05) {
            element.style.whiteSpace = 'normal';
            element.style.lineHeight = '1.2';
          }
        }
      });
    };

    const toggleEditing = (field) => {
      if (editing.value[field]) {
        cancelEditing(field)
      } else {
        startEditing(field)
      }
    }

    const startEditing = (field) => {
      editing.value = { ...editing.value, [field]: true }
      editableCard.value = { ...card.value }
      
      nextTick(() => {
        switch(field) {
          case 'name':
            nameInput.value?.focus()
            break
          case 'description':
            descriptionInput.value?.focus()
            break
          case 'category':
            categoryInput.value?.focus()
            break
        }
      })
    }

    const cancelEditing = (field) => {
      editing.value = { ...editing.value, [field]: false }
    }

    const saveField = async (field) => {
      try {
        const response = await fetch(`/api/cards/${card.value.uuid}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            [field]: editableCard.value[field]
          })
        })

        const contentType = response.headers.get('content-type')
        if (!contentType || !contentType.includes('application/json')) {
          const text = await response.text()
          throw new Error(text || 'Invalid server response')
        }

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || 'Failed to update card')
        }

        card.value = { ...card.value, [field]: editableCard.value[field] }
        editing.value = { ...editing.value, [field]: false }
      } catch (err) {
        console.error('Error updating card:', err)
        error.value = err.message || 'Failed to update card'
      }
    }

    const loadData = async () => {
      try {
        loading.value = true
        card.value = await fetchCardInfo(props.uuid)
        editableCard.value = { ...card.value }
        
        const season = await fetchSeasonInfo(card.value.season_id)
        seasonName.value = season.name
        
        comments.value = await fetchComments(card.value.id)
        
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

    return {
      card,
      editableCard,
      seasonName,
      comments,
      loading,
      error,
      imageError,
      cardNameRef,
      editing,
      toggleEditing,
      startEditing,
      cancelEditing,
      saveField,
      nameInput,
      descriptionInput,
      categoryInput
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

.card-header-section {
  margin-top: 64px;
  position: relative;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.title-container {
  position: absolute;
  bottom: 17px;
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
  transition: color 0.3s ease, box-shadow 0.3s ease;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

.main-divider {
  height: 2px;
  width: 100%;
  background-color: var(--card-border-color);
  top: 20%;
  position: relative;
  bottom: -20px;
}

.card-description-section {
  padding: 30px 0;
}

.card-description {
  font-size: 18px;
  line-height: 1.6;
  color: var(--text-color);
  text-align: center;
  position: relative;
}

.secondary-divider {
  height: 1px;
  width: 100%;
  background-color: var(--card-border-color);
  margin-top: 30px;
}

.card-info-section {
  padding: 0px 0;
}

.card-info-columns {
  display: flex;
  justify-content: space-around;
  gap: 20px;
}

.card-info-column {
  flex: 1;
  text-align: center;
  position: relative;
  padding: 20px;
  background-color: rgba(30, 30, 30, 0.7);
  border-radius: 12px;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-info-column h3 {
  font-size: 25px;
  margin-bottom: 15px;
  color: var(--accent-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.category-text {
  font-size: 22px;
  color: white;
  margin: 10px 0;
  padding: 10px 15px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  display: inline-block;
  min-width: 200px;
}

.category-input {
  font-size: 22px;
  color: white;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid var(--accent-color);
  border-radius: 8px;
  padding: 10px 15px;
  width: 100%;
  max-width: 300px;
  margin: 10px 0;
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

.edit-icon {
  margin-left: 10px;
  cursor: pointer;
  opacity: 0.7;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.05);
}

.edit-icon:hover {
  opacity: 1;
  background-color: rgba(255, 255, 255, 0.15);
  transform: scale(1.1);
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
  width: 80%;
}

.edit-textarea {
  font-size: inherit;
  font-family: inherit;
  color: inherit;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--accent-color);
  border-radius: 4px;
  padding: 10px;
  width: 100%;
  min-height: 100px;
  resize: vertical;
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
    font-size: 100px;
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

  .card-info-columns {
    flex-direction: column;
    gap: 15px;
  }

  .card-info-column {
    min-height: auto;
    padding: 15px;
  }

  .category-input {
    width: 100%;
    max-width: none;
  }
}
</style>