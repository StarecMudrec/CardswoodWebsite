<template>
  <div class="page-container">
    <div class="background-container"></div>
    <img src="/logo_noph.png" alt="Логотип" class="background-logo">
    <hr class="separator-line">

    <div class="content-wrapper">
      <section class="donate-section" aria-labelledby="donate-title">
        <div class="donate-header">
          <h1 id="donate-title" class="title">Поддержать проект</h1>
          <p class="subtitle">
            Выберите сумму — и вы будете перенаправлены на защищённую страницу оплаты PayAnyWay.
          </p>
        </div>

        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Сумма пожертвования</h2>
            <p class="card-subtitle">Выберите готовый вариант или укажите свой.</p>
          </div>

          <div class="amounts" role="list">
            <button
              v-for="preset in presets"
              :key="preset"
              type="button"
              class="amount-btn"
              :class="{ active: amount === preset }"
              @click="selectPreset(preset)"
            >
              {{ preset }} ₽
            </button>
          </div>

          <div class="custom-row">
            <label class="custom-label" for="custom-amount">Или введите свою сумму</label>
            <input
              id="custom-amount"
              v-model.number="customAmount"
              type="number"
              min="10"
              step="10"
              class="custom-input"
              placeholder="например, 300"
            />
          </div>

          <div class="actions">
            <button
              type="button"
              class="donate-btn"
              :disabled="loading || !validAmount"
              @click="startDonation"
            >
              <span v-if="loading">Перенаправляем...</span>
              <span v-else>Оплатить через PayAnyWay</span>
            </button>
          </div>

          <p v-if="error" class="error">{{ error }}</p>

          <p class="hint">
            Платежи обрабатываются PayAnyWay (MONETA.ru). Мы никогда не храним данные вашей карты на
            этом сайте.
          </p>
        </div>
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
      presets: [100, 300, 500],
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
    }
  },
  methods: {
    selectPreset (value) {
      this.amount = value
      this.customAmount = null
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
        this.error = e.message || 'Не удалось начать оплату'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.page-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%;
  z-index: 1;
}

.background-logo {
  position: absolute;
  top: 100px;
  left: 50%;
  transform: translate(-50%, 0);
  max-width: 250px;
  max-height: 250px;
  z-index: 1;
}

.separator-line {
  position: relative;
  margin-top: 47vh;
  height: 2px;
  background-color: white;
  border: none;
  z-index: 2;
  width: 75%;
}

.content-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 1;
  z-index: 2;
}

.donate-section {
  padding: 32px 16px 40px;
  width: min(720px, 100%);
  margin: 0 auto;
  color: var(--text-color, #fff);
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

.donate-header {
  margin-bottom: 16px;
}

.title {
  font-size: 40px;
  margin-bottom: 8px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.subtitle {
  margin-bottom: 12px;
  font-size: 18px;
  max-width: 520px;
}

.card {
  background: radial-gradient(circle at top left, rgba(255, 185, 71, 0.12), transparent 55%),
    rgba(0, 0, 0, 0.75);
  border-radius: 18px;
  padding: 24px 22px 22px;
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.card-header {
  margin-bottom: 18px;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 4px;
}

.card-subtitle {
  font-size: 14px;
  opacity: 0.85;
}

.amounts {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.amount-btn {
  flex: 1;
  min-width: 90px;
  padding: 10px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  background: rgba(0, 0, 0, 0.4);
  color: #fff;
  cursor: pointer;
  font-size: 15px;
  transition: background 0.2s ease, transform 0.1s ease, box-shadow 0.2s ease;
  white-space: nowrap;
}

.amount-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.7);
}

.amount-btn.active {
  background: #ffb947;
  color: #000;
  border-color: #ffb947;
}

.custom-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.custom-label {
  font-size: 14px;
}

.custom-input {
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  background: rgba(0, 0, 0, 0.4);
  color: #fff;
  outline: none;
  font-size: 16px;
}

.custom-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.actions {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 8px;
}

.donate-btn {
  padding: 10px 24px;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  background: linear-gradient(135deg, #ffb947, #ff7a3c);
  color: #000;
  font-size: 17px;
  font-weight: 600;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.7);
  transition: transform 0.1s ease, box-shadow 0.2s ease, opacity 0.2s ease;
}

.donate-btn:hover:enabled {
  transform: translateY(-1px);
  box-shadow: 0 10px 26px rgba(0, 0, 0, 0.8);
}

.donate-btn:disabled {
  opacity: 0.7;
  cursor: default;
}

.error {
  color: #ffb4b4;
  margin-top: 8px;
}

.hint {
  margin-top: 16px;
  font-size: 13px;
  max-width: 480px;
  color: rgba(255, 255, 255, 0.8);
}

@media (max-width: 1024px) {
  .separator-line {
    width: 90%;
  }

  .donate-section {
    padding-top: 24px;
  }
}

@media (max-width: 768px) {
  .background-logo {
    max-width: 200px;
    max-height: 200px;
    top: 90px;
  }

  .separator-line {
    margin-top: 42vh;
  }

  .donate-section {
    padding-inline: 12px;
  }

  .title {
    font-size: 30px;
  }

  .subtitle {
    font-size: 16px;
  }

  .card {
    padding: 20px 18px 18px;
  }

  .donate-btn {
    width: 100%;
    text-align: center;
    justify-content: center;
  }
}

@media (max-width: 600px) {
  .title {
    font-size: 28px;
  }

  .card {
    padding: 18px 16px 16px;
  }
}
</style>
