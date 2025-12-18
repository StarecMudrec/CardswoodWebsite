<template>
  <footer class="footer" role="contentinfo">
    <div class="footer-inner">
      <div class="footer-col">
        <h3 class="footer-title">Контакты</h3>
        <div class="footer-content">
          <div class="footer-item">
            <span class="footer-label">ФИО:</span>
            <span class="footer-text">Лукьянов Савелий Романович</span>
          </div>
          <div class="footer-item">
            <span class="footer-label">ИНН:</span>
            <span class="footer-text">772158474048</span>
          </div>
          <div class="footer-item">
            <span class="footer-label">Эл. почта:</span>
            <a class="footer-link" href="mailto:otect84@gmail.com" aria-label="Написать на электронную почту">
              <span class="link-icon">✉️</span>
              otect84@gmail.com
            </a>
          </div>
          <div class="footer-item">
            <span class="footer-label">Телеграм:</span>
            <a class="footer-link" href="https://t.me/youngmintman" target="_blank" rel="noopener noreferrer" aria-label="Перейти в Telegram">
              <span class="link-icon">📱</span>
              @youngmintman
            </a>
          </div>
        </div>
      </div>

      <div class="footer-col">
        <h3 class="footer-title">Документы</h3>
        <div class="footer-content">
          <a
            class="footer-link document-link"
            href="https://docs.google.com/document/d/1gYuOWR89EgNJZCpNleT5d8vDo2q6TTmb/edit"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Открыть договор оферты"
          >
            <span class="link-icon">📄</span>
            Договор оферты
          </a>
        </div>
      </div>

      <div class="footer-bottom">
        <div class="copyright">
          © {{ currentYear }} Все права защищены
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
  data() {
    return {
      currentYear: new Date().getFullYear()
    }
  }
}
</script>

<style scoped>
.footer {
  position: relative;
  z-index: 2;
  margin-top: 60px;
  padding: 32px 0 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.16);
  background: linear-gradient(180deg, rgba(18, 18, 18, 0.9) 0%, rgba(10, 10, 10, 0.95) 100%);
  backdrop-filter: blur(12px);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.2);
}

.footer-inner {
  width: min(1200px, 92vw);
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  color: var(--text-color, #fff);
}

.footer-col {
  padding: 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.footer-col:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-2px);
}

.footer-title {
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 16px;
  font-size: 1.3rem;
  color: var(--text-color, #fff);
  position: relative;
  padding-bottom: 8px;
}

.footer-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 2px;
  background: var(--accent-color, #4a90e2);
  border-radius: 2px;
}

.footer-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-item {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
}

.footer-label {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  min-width: 80px;
}

.footer-text {
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
}

.footer-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--accent-color, #4a90e2);
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
  background: rgba(74, 144, 226, 0.1);
  border: 1px solid transparent;
  font-weight: 500;
}

.footer-link:hover,
.footer-link:focus {
  color: var(--hover-color, #63a4ff);
  background: rgba(74, 144, 226, 0.2);
  border-color: rgba(74, 144, 226, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
  outline: none;
}

.footer-link:active {
  transform: translateY(0);
}

.link-icon {
  font-size: 1.1rem;
  opacity: 0.9;
}

.document-link {
  margin-top: 8px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.05);
  border-left: 3px solid var(--accent-color, #4a90e2);
}

.footer-bottom {
  grid-column: 1 / -1;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.copyright {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.85rem;
  letter-spacing: 0.3px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .footer {
    margin-top: 40px;
    padding: 24px 0 16px;
  }

  .footer-inner {
    gap: 24px;
    padding: 0 16px;
  }

  .footer-col {
    padding: 16px 12px;
  }

  .footer-title {
    font-size: 1.2rem;
  }

  .footer-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .footer-label {
    min-width: auto;
    font-size: 0.85rem;
  }

  .footer-link {
    padding: 8px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .footer {
    padding: 20px 0 12px;
  }

  .footer-inner {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .footer-col {
    padding: 14px;
  }

  .footer-title {
    font-size: 1.1rem;
    margin-bottom: 12px;
  }

  .footer-link {
    width: 100%;
    justify-content: center;
    padding: 10px;
  }

  .document-link {
    justify-content: flex-start;
    padding-left: 12px;
  }
}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .footer-col,
  .footer-link {
    transition: none;
    transform: none;
  }
}

/* Dark mode adjustments */
@media (prefers-color-scheme: light) {
  .footer {
    background: linear-gradient(180deg, rgba(240, 240, 240, 0.95) 0%, rgba(255, 255, 255, 0.98) 100%);
    border-top: 1px solid rgba(0, 0, 0, 0.1);
  }

  .footer-col {
    background: rgba(0, 0, 0, 0.02);
  }

  .footer-col:hover {
    background: rgba(0, 0, 0, 0.05);
  }

  .footer-title,
  .footer-label {
    color: #333;
  }

  .footer-text {
    color: #666;
  }

  .footer-link {
    background: rgba(74, 144, 226, 0.08);
  }

  .document-link {
    background: rgba(0, 0, 0, 0.03);
  }

  .footer-bottom {
    border-top: 1px solid rgba(0, 0, 0, 0.1);
  }

  .copyright {
    color: #888;
  }
}
</style>