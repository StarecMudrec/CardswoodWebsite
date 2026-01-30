<template>
  <div class="page-container">
    <div class="background-container" aria-hidden="true"></div>
    <img src="/logo_noph.png" alt="Логотип" class="background-logo">
    <div class="background-overlay" aria-hidden="true"></div>

    <div class="content-wrapper">
      <main class="shop-section" aria-labelledby="shop-title">
        <header class="shop-header">
          <h1 id="shop-title" class="title">Магазин Cardswood</h1>
          <div class="separator-line" aria-hidden="true"></div>
        </header>

        <section ref="productsGrid" class="products-grid" aria-label="Каталог товаров">
          <div 
            v-for="product in products" 
            :key="product.id"
            class="product-card glass-effect"
            :data-product-id="product.id"
          >
            <div class="product-image-container">
              <img 
                :src="product.image" 
                :alt="product.name" 
                class="product-image"
                @error="handleImageError"
              >
            </div>
            
            <div class="product-content">
              <h3 class="product-name">{{ product.name }}</h3>
              <div class="product-description-wrapper">
                <p 
                  class="product-description" 
                  :class="{ 'expanded': expandedDescriptions[product.id] }"
                >{{ product.description }}</p>
                <button 
                  v-if="needsExpansion(product.id)"
                  class="read-more-btn"
                  @click="toggleDescription(product.id)"
                >
                  {{ expandedDescriptions[product.id] ? 'Свернуть' : 'Развернуть' }}
                </button>
              </div>
              
              <div class="product-footer">
                <div class="product-price">
                  <span class="price-value">{{ product.price.toLocaleString('ru-RU') }}₽</span>
                  <!-- <span class="currency">₽</span> -->
                </div>
                
                <button 
                  class="buy-btn"
                  :disabled="product.loading"
                  @click="addToCart(product)"
                >
                  <span v-if="product.loading" class="spinner"></span>
                  <template v-else>
                    <img src="/shopping-cart.svg" class="cart-icon" alt="" />
                    В корзину
                  </template>
                </button>
              </div>
            </div>
          </div>
        </section>

        <aside class="cart-section glass-effect" v-if="cart.length > 0" aria-label="Корзина">
          <h2 class="cart-title">Ваша корзина</h2>
          <div class="cart-items">
            <div v-for="item in cart" :key="item.id" class="cart-item">
              <div class="cart-item-info">
                <span class="cart-item-name">{{ item.name }}</span>
                <span class="cart-item-price">{{ item.price.toLocaleString('ru-RU') }} ₽</span>
              </div>
              <button class="remove-btn" @click="removeFromCart(item.id)">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41Z" fill="currentColor"/>
                </svg>
              </button>
            </div>
          </div>
          <div class="cart-total">
            <span>Итого:</span>
            <span class="total-amount">{{ totalAmount.toLocaleString('ru-RU') }} ₽</span>
          </div>
          <button class="checkout-btn" @click="proceedToCheckout" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <template v-else>Перейти к оплате</template>
          </button>
        </aside>

        <div v-if="error" class="error-message glass-effect" role="alert">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="#ff6b6b"/>
          </svg>
          <span>{{ error }}</span>
        </div>

        <!-- <section class="features glass-effect" aria-label="Преимущества">
          <div class="feature-item">
            <div class="feature-icon">🚚</div>
            <h3 class="feature-title">Мгновенная доставка</h3>
            <p class="feature-text">Цифровые товары доступны сразу после оплаты</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🔒</div>
            <h3 class="feature-title">Безопасная оплата</h3>
            <p class="feature-text">Защищённые платежи</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🎮</div>
            <h3 class="feature-title">Улучшите игру</h3>
            <p class="feature-text">Эксклюзивный контент для лучшего опыта</p>
          </div>
        </section> -->

      </main>

      <footer class="page-footer">
        <Footer />
      </footer>
    </div>
  </div>
</template>

<script>
import Footer from '@/components/Footer.vue'
import { createOrder } from '@/api'

export default {
  name: 'ShopView',
  components: {
    Footer
  },
  data() {
    return {
      products: [
        {
          id: 1,
          name: 'ПОДПИСКА CARDSWOOD',
          description: 'Наша подписка даёт следующие привилегии при покупке:\n\n- ВРЕМЯ ОЖИДАНИЯ НОВОЙ КАРТЫ СНИЖЕНО ДО 3 ЧАСОВ\n- ВРЕМЯ ОЖИДАНИЯ ОБЫЧНОГО ПАКА СНИЖЕНО ДО 12 ЧАСОВ\n- ВЫДАЧА 1 ЭКСКЛЮЗИВНОЙ СПЕШЛ КАРТЫ В МЕСЯЦ\n- ВОЗМОЖНОСТЬ БРОСИТЬ 2 КУБИКА В НЕДЕЛЮ\n- ВОЗМОЖНОСТЬ ОТКРЫТЬ1 ПИСЬМО В ДЕНЬ\n- ВОЗМОЖНОСТЬ СЫГРАТЬ В БОУЛИНГ 1 РАЗ В ДЕНЬ\n\nВсе преимущества подписка даёт ровно на 30 дней!',
          price: 99,
          image: '/cw_sub_lvl1.jpg',
          tag: 'Популярное'
        },
        {
          id: 2,
          name: 'ПОДПИСКА CARDSWOOD PREMIUM',
          description: 'При покупке подписка премиум дает намного больше преимуществ чем обычная подписка, а именно:\n\n- ВРЕМЯ ОЖИДАНИЯ НОВОЙ КАРТЫ СНИЖЕНО ДО 2 ЧАСОВ\n- ВОЗМОЖНОСТЬ ОТКРЫТЬ 1 РАЗ В ДЕНЬ ЛЮКС-ПАК\n- ВРЕМЯ ОЖИДАНИЯ ОБЫЧНОГО ПАКА СНИЖЕНО ДО 12 ЧАСОВ\n- ВЫДАЧА ДВУХ ЭКСКЛЮЗИВНЫХ СПЕШЛ КАРТ В МЕСЯЦ\n- ВОЗМОЖНОСТЬ БРОСИТЬ 1 КУБИК В ДЕНЬ\n- ВОЗМОНОСТЬ ОТКРЫТЬ 2 ПИСЬМА В ДЕНЬ\n- ВОЗМОЖНОСТЬ СЫГРАТЬ В БОУЛИНГ 1 РАЗ В ДЕНЬ\n- ВОЗМОЖНОСТЬ СЫГРТЬ В ДАРТС 1 РАЗ В ДЕНЬ\n\nВсе привилегии действуют также ровно 30 дней!',
          price: 199,
          image: '/cw_sub_lvl2.jpg',
          tag: 'Выгодно'
        },
        {
          id: 3,
          name: 'ОБЫЧНЫЙ ПАК',
          description: 'При покупке вы гарантировано получите 🍿Попкорн и карты разных редкостей, а именно:\n\n- 3 карты редкости от EPISODICAL до FAMOUS\n- 1 карту случайной редкости\n- 1 карту редкости MOVIE или SERIES',
          price: 29,
          image: '/regular_pack.png',
          tag: 'Лимитированно'
        },
        {
          id: 4,
          name: 'РЕДКИЙ ПАК',
          description: 'При покупке вы гарантировано получите 🍿Попкорн и карты разных редкостей, а именно:\n\n- 4 карты случайной редкости\n- 1 карта редкости MOVIE или SERIES\n\nТакже в этом паке повышенные шансы на получение большего количества Попкорна!',
          price: 69,
          image: '/rare_pack.png',
          tag: 'Сезонное'
        },
        {
          id: 6,
          name: 'ЭПИЧЕСКИЙ ПАК',
          description: 'Пак с самыми ценными наградами, отсюда вы получите самые редкие карты в игре и самое большое количество Попкорна:\n\n- 2 карты случайной редкости\n- 3 карты MOVIE или SERIES',
          price: 109,
          image: '/epic_pack.png',
          tag: 'Классика'
        },
        {
          id: 5,
          name: 'MOVIE HOME ALONE',
          description: 'Фильм, определивший рождественское кино для целого поколения. Занял 1 место в прокате 1990 года. Эта карта — напоминание, что даже самый маленький герой может всех перехитрить. Коллекционный must-have для любого ценителя комедий и рождественского настроения! Данная карта была доступна к получению только в новогодний ивент!\n\nВнимание, карта не будет постоянно находиться в продаже и её тираж будет ограничен!',
          price: 99,
          image: '/ha.jpg',
          tag: 'Легендарная'
        }
      ],
      cart: [],
      loading: false,
      error: null,
      expandedDescriptions: {}
    }
  },
  computed: {
    totalAmount() {
      return this.cart.reduce((sum, item) => sum + item.price, 0)
    }
  },
  methods: {
    handleImageError(event) {
      event.target.src = '/logo_noph.png'
    },
    toggleDescription(productId) {
      const newState = !this.expandedDescriptions[productId]
      
      // Find all products in the same row
      this.$nextTick(() => {
        const grid = this.$refs.productsGrid
        if (!grid) return
        
        const clickedCard = grid.querySelector(`[data-product-id="${productId}"]`)
        if (!clickedCard) return
        
        // Get the clicked card's position
        const clickedRect = clickedCard.getBoundingClientRect()
        const clickedTop = clickedRect.top
        
        // Find all cards in the same row (same top position, with some tolerance)
        const allCards = grid.querySelectorAll('.product-card')
        const rowTolerance = 10 // pixels tolerance for same row detection
        
        allCards.forEach(card => {
          const cardRect = card.getBoundingClientRect()
          const cardTop = cardRect.top
          
          // Check if card is in the same row
          if (Math.abs(cardTop - clickedTop) < rowTolerance) {
            const cardProductId = parseInt(card.getAttribute('data-product-id'))
            if (cardProductId) {
              this.expandedDescriptions[cardProductId] = newState
            }
          }
        })
      })
    },
    needsExpansion(productId) {
      // Check if description is long enough to need expansion
      const product = this.products.find(p => p.id === productId)
      if (!product) return false
      // Approximate check: if description has more than ~150 characters, it likely needs expansion
      return product.description.length > 150
    },
    addToCart(product) {
      this.loading = true
      this.error = null
      
      // Check if product is already in cart
      if (this.cart.some(item => item.id === product.id)) {
        this.error = 'Этот товар уже в корзине'
        this.loading = false
        return
      }
      
      // Simulate API call
      setTimeout(() => {
        this.cart.push({
          id: product.id,
          name: product.name,
          price: product.price
        })
        this.loading = false
        
        // Show success message
        this.$notify({
          title: 'Добавлено в корзину',
          message: `${product.name} успешно добавлен в корзину`,
          type: 'success'
        })
      }, 300)
    },
    removeFromCart(productId) {
      this.cart = this.cart.filter(item => item.id !== productId)
    },
    async proceedToCheckout() {
      if (this.cart.length === 0) {
        this.error = 'Корзина пуста'
        return
      }
      this.error = null
      this.loading = true
      try {
        const data = await createOrder(this.cart)
        if (data.payment_url) {
          window.location.href = data.payment_url
          return
        }
        this.error = 'Не получена ссылка на оплату'
      } catch (err) {
        this.error = err.message || 'Ошибка при оформлении заказа'
        console.error(err)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.page-container,
.page-container * {
  font-family: "Tinos", serif !important;
}

.page-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
}

.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 450px;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%;
  z-index: 1;
  opacity: 0.7;
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 450px;
  background: linear-gradient(to bottom, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.4) 100%);
  z-index: 1;
}

.background-logo {
  position: absolute;
  top: 120px;
  left: 50%;
  transform: translate(-50%, 0);
  width: 30vh;
  aspect-ratio: 1;
  z-index: 2;
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.5));
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(-50%, 0) translateY(0px); }
  50% { transform: translate(-50%, 0) translateY(-10px); }
}

.separator-line {
  position: relative;
  /* margin-top: 45vh; */
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(255, 185, 71, 0.5), transparent);
  border: none;
  z-index: 3;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}

.content-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 1;
  z-index: 3;
}

.page-footer {
  position: relative;
  z-index: 3;
}

.shop-section {
  padding: 48px 16px 60px;
  width: min(1200px, 100%);
  margin: 0 auto;
  margin-top: 45vh;
  color: #fff;
}

.shop-header {
  text-align: center;
  margin-bottom: 48px;
}

.header-icon {
  margin-bottom: 20px;
  animation: pulse 2s infinite;
}

.header-cart-icon {
  width: 48px;
  height: 48px;
  display: inline-block;
  background: linear-gradient(135deg, var(--gradient-color) 0%, var(--gradient-color-sec) 100%);
  -webkit-mask: url('/shopping-cart.svg') no-repeat center / contain;
  mask: url('/shopping-cart.svg') no-repeat center / contain;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.title {
  font-size: 48px;
  margin-bottom: 16px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  background: linear-gradient(135deg, var(--gradient-color) 0%, var(--gradient-color-sec) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
}

.subtitle {
  margin: 0 auto 24px;
  font-size: 18px;
  max-width: 600px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.glass-effect {
  background: rgba(30, 30, 30, 0.8);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card {
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 25px 70px rgba(0, 0, 0, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.product-image-container {
  position: relative;
  height: 450px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

.product-tag {
  position: absolute;
  top: 12px;
  right: 12px;
  background: linear-gradient(135deg, var(--gradient-color) 0%, var(--gradient-color-sec) 100%);
  color: #000;
  font-size: 12px;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.product-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 0;
  margin-top: 0;
  color: #fff;
  line-height: 1.3;
}

.product-description-wrapper {
  flex: 1;
  margin-top: 10px;
  margin-bottom: 10px;
}

.product-description {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
  margin: 0;
  white-space: pre-line;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.3s ease;
}

.product-description.expanded {
  display: block;
  -webkit-line-clamp: unset;
  line-clamp: unset;
  overflow: visible;
}

.read-more-btn {
  background: transparent;
  border: none;
  color: var(--gradient-color);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 0;
  margin-top: 4px;
  text-decoration: underline;
  transition: opacity 0.3s ease;
  font-family: "Tinos", serif;
}

.read-more-btn:hover {
  opacity: 0.8;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.product-price {
  display: flex;
  align-items: baseline;
}

.price-value {
  font-size: 35px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--gradient-color) 0%, var(--gradient-color-sec) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.currency {
  font-size: 35px;
  font-weight: 600;
  color: var(--gradient-color);
  margin-left: 4px;
}

.buy-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, var(--gradient-color) 0%, var(--gradient-color-sec) 100%);
  color: #000;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-shadow: 0 2px 6px #00000073;
}

.buy-btn:hover:enabled {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 185, 71, 0.3);
}

.buy-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.cart-icon {
    width: 22px;
    height: 22px;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 3px solid rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  border-top-color: #000;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.cart-section {
  padding: 24px;
}

.cart-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 20px;
  color: #fff;
}

.cart-items {
  margin-bottom: 20px;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 20px;
}

.cart-item-info {
  display: flex;
  justify-content: space-between;
  flex: 1;
  margin-right: 10px;
}

.cart-item-name {
  color: #fff;
  font-weight: 500;
}

.cart-item-price {
  color: var(--gradient-color);
  font-weight: 600;
  font-size: 22px;
}

.remove-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: color 0.3s ease;
  display: flex;
}

.remove-btn:hover {
  color: #ff6b6b;
}

.cart-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  font-size: 25px;
  font-weight: 600;
  color: #fff;
}

.total-amount {
  font-size: 25px;
  color: var(--gradient-color);
}

.checkout-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #4cd964 0%, #2ecc71 100%);
  color: #000;
  border: none;
  border-radius: 16px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 16px;
  text-shadow: 0 2px 6px #00000073;
}

.checkout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(76, 217, 100, 0.3);
}

.error-message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  border-radius: 12px;
  margin-bottom: 24px;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  padding: 32px;
  margin-top: 40px;
}

.feature-item {
  text-align: center;
  padding: 24px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: transform 0.3s ease, background 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 185, 71, 0.2);
}

.feature-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #fff;
}

.feature-text {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .separator-line {
    width: 90%;
  }
  
  .title {
    font-size: 42px;
  }
  
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}

@media (max-width: 768px) {
  .background-logo {
    width: 140px;
    height: 140px;
    top: 100px;
  }
  
  .separator-line {
    margin-top: 40vh;
  }
  
  .shop-section {
    padding: 32px 16px 48px;
  }
  
  .title {
    font-size: 36px;
  }
  
  .subtitle {
    font-size: 16px;
  }
  
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
  
  .features {
    grid-template-columns: 1fr;
    padding: 24px;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 32px;
  }
  
  .products-grid {
    grid-template-columns: 1fr;
  }
  
  .price-value {
    font-size: 20px;
  }
  
  .buy-btn {
    padding: 8px 16px;
    font-size: 13px;
  }
}
</style>