<template>
  <div class="page-container">
    <div class="background-container"></div>
    <img src="/logo_noph.png" alt="Логотип" class="background-logo">
    <div class="background-overlay"></div>
    <div class="separator-line"></div>

    <div class="content-wrapper">
      <section class="donate-section" aria-labelledby="donate-title">
        <div class="donate-header">
          <div class="header-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.04L12 21.35Z" fill="#ffb947"/>
            </svg>
          </div>
          <h1 id="donate-title" class="title">Поддержать проект</h1>
          <p class="subtitle">
            Ваша поддержка помогает нам развиваться. Выберите сумму — и вы будете перенаправлены на защищённую страницу оплаты PayAnyWay.
          </p>
        </div>

        <div class="card glass-effect">
          <div class="card-header">
            <div class="header-content">
              <h2 class="card-title">Сумма пожертвования</h2>
              <p class="card-subtitle">Выберите готовый вариант или укажите свою сумму</p>
            </div>
            <div class="amount-preview">
              <span class="amount-value">{{ formattedAmount }}</span>
              <span class="currency">₽</span>
            </div>
          </div>

          <div class="preset-section">
            <div class="section-label">Быстрый выбор</div>
            <div class="amounts-grid" role="list">
              <button
                v-for="preset in presets"
                :key="preset"
                type="button"
                class="preset-btn"
                :class="{ active: amount === preset && !customAmount }"
                @click="selectPreset(preset)"
              >
                <span class="preset-amount">{{ preset }}</span>
                <span class="preset-currency">₽</span>
                <span class="preset-badge" v-if="preset === 300">Рекомендуемая</span>
              </button>
            </div>
          </div>

          <div class="custom-section">
            <div class="section-label">Своя сумма</div>
            <div class="custom-input-wrapper">
              <div class="input-prefix">₽</div>
              <input
                id="custom-amount"
                v-model.number="customAmount"
                type="number"
                min="10"
                step="10"
                class="custom-input"
                placeholder="Введите сумму"
                @focus="clearPreset"
              />
              <div class="input-suffix">.00</div>
            </div>
            <div class="input-hint">Минимальная сумма: 10 ₽</div>
          </div>

          <div class="actions">
            <button
              type="button"
              class="donate-btn"
              :disabled="loading || !validAmount"
              @click="startDonation"
            >
              <div class="btn-content">
                <span class="btn-icon">
                  <svg v-if="!loading" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="currentColor"/>
                  </svg>
                  <span v-else class="spinner"></span>
                </span>
                <span class="btn-text">
                  <template v-if="loading">Перенаправляем...</template>
                  <template v-else>Поддержать {{ formattedAmount }}</template>
                </span>
              </div>
              <div class="btn-subtext">Безопасная оплата через PayAnyWay</div>
            </button>
          </div>

          <div v-if="error" class="error-message">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="#ff6b6b"/>
            </svg>
            <span>{{ error }}</span>
          </div>

          <div class="security-info">
            <div class="security-header">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 1L3 5V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V5L12 1ZM12 11.99H19C18.47 16.11 15.72 19.78 12 20.93V12H5V6.3L12 3.19V11.99Z" fill="#4cd964"/>
              </svg>
              <span>Безопасные платежи</span>
            </div>
            <p class="security-text">
              Платежи обрабатываются PayAnyWay (MONETA.ru). Мы никогда не храним данные вашей карты на этом сайте. Все транзакции защищены 256-битным SSL-шифрованием.
            </p>
          </div>
        </div>

        <!-- <div class="features">
          <div class="feature-item">
            <div class="feature-icon">🎁</div>
            <h3 class="feature-title">Благодарность</h3>
            <p class="feature-text">Вы получите именную благодарность на сайте</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">📢</div>
            <h3 class="feature-title">Отчёты</h3>
            <p class="feature-text">Регулярные отчёты о расходовании средств</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">💝</div>
            <h3 class="feature-title">Сделайте вклад</h3>
            <p class="feature-text">Ваша поддержка помогает реализовать новые идеи</p>
          </div>
        </div> -->
      </section>

      <Footer />
    </div>
  </div>
</template>

<script>
import { createDonation } from '@/api'
import Footer from '@/components/Footer.vue'

export default {
  name: 'DonationView',
  components: {
    Footer
  },
  data () {
    return {
      presets: [100, 300, 500, 1000],
      amount: 300,
      customAmount: null,
      loading: false,
      error: null
    }
  },
  computed: {
    effectiveAmount () {
      if (this.customAmount && this.customAmount > 0) {
        return this.customAmount
      }
      return this.amount
    },
    validAmount () {
      return this.effectiveAmount && this.effectiveAmount > 0
    },
    formattedAmount () {
      return new Intl.NumberFormat('ru-RU').format(this.effectiveAmount)
    }
  },
  methods: {
    selectPreset (value) {
      this.amount = value
      this.customAmount = null
      this.error = null
    },
    clearPreset() {
      this.amount = null
      this.error = null
    },
    async startDonation () {
      if (!this.validAmount || this.loading) return
      this.loading = true
      this.error = null

      try {
        const { paymentUrl } = await createDonation(this.effectiveAmount, 'Пожертвование')
        if (paymentUrl) {
          window.location.href = paymentUrl
        } else {
          this.error = 'Сервер не вернул ссылку на оплату'
        }
      } catch (e) {
        console.error(e)
        this.error = e.message || 'Не удалось начать оплату. Пожалуйста, попробуйте позже.'
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
  width: 16%;
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
  margin-top: 45vh;
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

.donate-section {
  padding: 48px 16px 60px;
  width: min(800px, 100%);
  margin: 0 auto;
  color: #fff;
}

.donate-header {
  text-align: center;
  margin-bottom: 48px;
}

.header-icon {
  margin-bottom: 20px;
  animation: pulse 2s infinite;
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
  background: linear-gradient(135deg, #ffb947 0%, #ff7a3c 100%);
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

.glass-effect {
  background: rgba(30, 30, 30, 0.8);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 32px;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  margin-bottom: 40px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-effect:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 25px 70px rgba(0, 0, 0, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  flex: 1;
}

.card-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #fff;
}

.card-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.amount-preview {
  text-align: right;
  padding-left: 20px;
}

.amount-value {
  font-size: 42px;
  font-weight: 800;
  background: linear-gradient(135deg, #ffb947 0%, #ff7a3c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.currency {
  font-size: 24px;
  font-weight: 600;
  color: #ffb947;
  margin-left: 4px;
}

.preset-section {
  margin-bottom: 32px;
}

.section-label {
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 16px;
}

.amounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.preset-btn {
  position: relative;
  padding: 20px 16px;
  border-radius: 16px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.3);
  color: #fff;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.preset-btn:hover {
  border-color: rgba(255, 185, 71, 0.3);
  background: rgba(255, 185, 71, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 185, 71, 0.15);
}

.preset-btn.active {
  border-color: #ffb947;
  background: rgba(255, 185, 71, 0.15);
  box-shadow: 0 8px 25px rgba(255, 185, 71, 0.25);
}

.preset-amount {
  font-size: 24px;
  font-weight: 700;
}

.preset-currency {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
}

.preset-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: linear-gradient(135deg, #ffb947 0%, #ff7a3c 100%);
  color: #000;
  font-size: 10px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 12px;
  white-space: nowrap;
}

.custom-section {
  margin-bottom: 40px;
}

.custom-input-wrapper {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 8px 20px;
  transition: border-color 0.3s ease;
  margin-bottom: 8px;
}

.custom-input-wrapper:focus-within {
  border-color: #ffb947;
  box-shadow: 0 0 0 3px rgba(255, 185, 71, 0.1);
}

.input-prefix, .input-suffix {
  font-size: 20px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

.custom-input {
  flex: 1;
  padding: 6px 12px;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 22px;
  font-weight: 700;
  text-align: center;
  outline: none;
  min-width: 0;
}

.custom-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.input-hint {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
}

.actions {
  margin-bottom: 24px;
}

.donate-btn {
  width: 100%;
  padding: 24px 32px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  background: linear-gradient(135deg, #ffb947 0%, #ff7a3c 100%);
  color: #000;
  font-size: 18px;
  font-weight: 700;
  box-shadow: 0 12px 30px rgba(255, 185, 71, 0.3);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.donate-btn:hover:enabled {
  transform: translateY(-2px);
  box-shadow: 0 18px 40px rgba(255, 185, 71, 0.4);
}

.donate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.donate-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: 0.5s;
}

.donate-btn:hover:enabled::before {
  left: 100%;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 8px;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  border-top-color: #000;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.btn-text {
  font-size: 20px;
}

.btn-subtext {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.7);
  font-weight: 500;
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

.security-info {
  padding: 20px;
  background: rgba(76, 217, 100, 0.05);
  border: 1px solid rgba(76, 217, 100, 0.2);
  border-radius: 16px;
}

.security-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  font-weight: 600;
  color: #4cd964;
}

.security-text {
  font-size: 14px;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
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
  
  .donate-section {
    padding: 32px 16px 48px;
  }
  
  .title {
    font-size: 36px;
  }
  
  .subtitle {
    font-size: 16px;
  }
  
  .glass-effect {
    padding: 24px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .amount-preview {
    width: 100%;
    text-align: left;
    padding-left: 0;
  }
  
  .amounts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .features {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 32px;
  }
  
  .glass-effect {
    padding: 20px 16px;
  }
  
  .amounts-grid {
    grid-template-columns: 1fr;
  }
  
  .amount-value {
    font-size: 36px;
  }
  
  .custom-input {
    font-size: 28px;
    padding: 12px 8px;
  }
  
  .donate-btn {
    padding: 20px 24px;
  }
  
  .btn-text {
    font-size: 18px;
  }
}
</style>
