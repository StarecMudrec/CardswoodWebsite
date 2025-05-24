<template>
  <div class="add-card-background">
    <div class="add-card-container">
      <h1>Add New Card</h1>
      <form @submit.prevent="submitForm" class="card-form">
        <div class="form-group">
          <label for="name">Card Name:</label>
          <input type="text" id="name" v-model="card.name" required>
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" v-model="card.description" required></textarea>
        </div>
        <div class="form-group">
          <label for="category">Category:</label>
          <input type="text" id="category" v-model="card.category" required>
        </div>
        <div class="form-group">
          <label for="season">Season:</label>
          <input type="number" id="season" v-model="card.season" required>
        </div>
        <div class="form-group">
          <label for="image">Card Image:</label>
          <input type="file" id="image" @change="handleFileUpload" accept="image/*" required>
        </div>
        <button type="submit" class="submit-button">Add Card</button>
      </form>
      <router-link to="/" class="back-link">← Back to home</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      card: {
        name: '',
        description: '',
        category: '',
        season: null,
        image: null
      }
    };
  },
  methods: {
    handleFileUpload(event) {
      this.card.image = event.target.files[0];
    },
    async submitForm() {
      const formData = new FormData();
      const cardUuid = this.uuidv4(); // Generate UUID
      formData.append('uuid', cardUuid);
      formData.append('name', this.card.name);
      formData.append('description', this.card.description);
      formData.append('category', this.card.category);
      formData.append('season_id', this.card.season);
      formData.append('img', this.card.image);

      try {
        const response = await axios.post('/api/cards', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Card added successfully:', response.data);
        this.resetForm();
      } catch (error) {
        console.error('Error adding card:', error);
      }
    },
    resetForm() {
      this.card = {
        name: '',
        description: '',
        category: '',
        season: null,
        image: null
      };
      const fileInput = document.getElementById('image');
      if (fileInput) {
        fileInput.value = '';
      }
    }
  },
  setup() {
    // Function to generate a random UUID (v4)
    const uuidv4 = () => {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    };
    return {
      uuidv4
    };
  }
};
</script>

<style scoped>
.add-card-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 95%;
  z-index: 1;
}

.add-card-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  box-sizing: border-box;
  max-width: 500px;
  padding: 40px;
  background-color: var(--card-bg);
  border-radius: 17px;
  border: 1px solid var(--border-color);
  text-align: center;
}

h1 {
  color: var(--accent-color);
  font-weight: 500;
  margin-bottom: 25px;
  font-size: 28px;
}

.card-form {
  text-align: left;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: var(--accent-color);
  font-weight: 500;
}

input[type="text"],
input[type="number"],
textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 16px;
}

textarea {
  min-height: 100px;
  resize: vertical;
}

input[type="file"] {
  width: 100%;
  padding: 12px 0;
  color: var(--accent-color);
}

.submit-button {
  width: 100%;
  padding: 14px;
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: var(--hover-color);
}

.back-link {
  display: inline-block;
  margin-top: 25px;
  color: var(--accent-color);
  text-decoration: none;
  font-size: 17px;
  position: relative;
  padding-bottom: 2px;
}

.back-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: var(--accent-color);
  transition: width 0.3s ease;
}

.back-link:hover::after {
  width: 100%;
}

@media (max-width: 600px) {
  .add-card-container {
    padding: 30px 20px;
    max-width: 90%;
  }
  
  h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  input[type="text"],
  input[type="number"],
  textarea {
    padding: 10px;
    font-size: 14px;
  }
  
  .submit-button {
    padding: 12px;
    font-size: 15px;
  }
  
  .back-link {
    font-size: 15px;
  }
}
</style>