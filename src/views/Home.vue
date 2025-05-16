<template>
    <div class="home">
      <div class="menu">
        <router-link href="/home">CARDS</router-link> | 
        <router-link href="/termins">TERMINS</router-link> | 
        <router-link v-if="isAuth" to="/auth/logout">LOGOUT</router-link>
        <router-link v-else to="/login">LOGIN</router-link>
      </div>
  
      <div v-for="season in seasons" :key="season.uuid" class="season">
        <h2>{{ season.name }}</h2>
        <div class="cards">
          <!-- <Card
            v-for="(card, uuid) in cards[season.uuid]"
            :key="uuid"
            :uuid="uuid"
            :img="card"
            @click="goToCard(uuid)"
          /> -->
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios';
import Card from '../components/Card.vue';

export default {
    components: { Card },
    data() {
        return {
            seasons: [],
            cards: {},
            isAuth: false, // Здесь нужно будет добавить логику проверки авторизации
        };
    },
    async created() {
        // Получаем список сезонов
        const seasonsResponse = await axios.get('/api/seasons');
        this.seasons = seasonsResponse.data;

        // Для каждого сезона получаем карточки
        for (const season of this.seasons) {
            const cardsResponse = await axios.get(`/api/cards/${season.uuid}`);
            this.cards[season.uuid] = cardsResponse.data;
        }
    },
    methods: {
        goToCard(uuid) {
            this.$router.push(`/card/${uuid}`);
        },
    },
};
</script>

<style scoped>
    .home {
        padding: 20px;
    }

    .menu {
        margin-bottom: 20px;
    }

    .season {
        margin-bottom: 40px;
    }

    .cards {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
</style>