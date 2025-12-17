<template>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-col">
        <div class="footer-title">Контакты</div>
        <div class="footer-text">Лукьянов Савелий Романович</div>
        <div class="footer-text">ИНН: 772158474048</div>
        <div class="footer-text">
          Эл. почта:
          <a class="footer-link" href="mailto:otect84@gmail.com">otect84@gmail.com</a>
        </div>
        <div class="footer-text">
          Телеграм:
          <a class="footer-link" href="https://t.me/youngmintman" target="_blank" rel="noopener noreferrer">@youngmintman</a>
        </div>
      </div>

      <div class="footer-col">
        <div class="footer-title">Документы</div>
        <a
          class="footer-link"
          href="https://docs.google.com/document/d/1gYuOWR89EgNJZCpNleT5d8vDo2q6TTmb/edit"
          target="_blank"
          rel="noopener noreferrer"
        >
          Договор оферты
        </a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  position: relative;
  z-index: 2;
  margin-top: 40px;
  padding: 22px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(18, 18, 18, 0.65);
  backdrop-filter: blur(10px);
}

.footer-inner {
  width: min(1000px, 92vw);
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.25fr 0.75fr;
  gap: 18px 28px;
  color: var(--text-color);
}

.footer-title {
  font-weight: 600;
  letter-spacing: 0.2px;
  margin-bottom: 8px;
}

.footer-text {
  line-height: 1.45;
  opacity: 0.92;
  margin: 3px 0;
}

.footer-link {
  color: var(--accent-color);
  text-decoration: none;
  opacity: 0.95;
}

.footer-link:hover {
  color: var(--hover-color);
}

@media (max-width: 640px) {
  .footer-inner {
    grid-template-columns: 1fr;
  }
}
</style>


