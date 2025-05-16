<template>
    <div class="card" @click="handleClick">
      <img :src="imgSrc" :alt="uuid" />
    </div>
  </template>
  
  <script>
  export default {
    props: {
      uuid: String,
      img: String,
    },
    computed: {
      imgSrc() {
        return `/cards_imgs/${this.img}`;
      },
    },
    methods: {
      handleClick() {
        this.$emit('click');
      },
    },
  };
  </script>
  
  <style scoped>
  .card {
    cursor: pointer;
    width: 150px;
    height: 200px;
    border: 1px solid #ccc;
    border-radius: 8px;
    overflow: hidden;
  }
  
  .card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  </style>