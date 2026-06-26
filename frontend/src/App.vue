<template>
  <div id="app-container">
    <header class="app-header">
      <div class="header-inner">
        <router-link to="/" class="logo">
          <span class="logo-icon">🎓</span>
          <span class="logo-text">智选大学</span>
        </router-link>
        <nav class="nav-links">
          <router-link to="/score-input">智能推荐</router-link>
          <router-link to="/universities">院校库</router-link>
          <router-link to="/volunteer-plan">志愿规划</router-link>
          <router-link to="/score-query">分数查询</router-link>
        </nav>
        <div class="header-slogan">不止看总分，按单科强项匹配最适合你的大学专业</div>
      </div>
    </header>
    <main class="app-main">
      <router-view />
    </main>
    <footer class="app-footer">
      <p>数据仅供参考，以各省教育考试院官方发布为准 | 智选大学 &copy; 2026</p>
    </footer>
  </div>
</template>

<script setup>
// App shell
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: white;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}
.header-inner {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 64px;
  gap: 32px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: white;
  font-weight: bold;
  font-size: 20px;
  flex-shrink: 0;
}
.logo-icon { font-size: 28px; }
.nav-links {
  display: flex;
  gap: 24px;
}
.nav-links a {
  color: rgba(255,255,255,0.75);
  text-decoration: none;
  font-size: 15px;
  padding: 4px 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}
.nav-links a:hover,
.nav-links a.router-link-active {
  color: white;
  border-bottom-color: #e94560;
}
.header-slogan {
  margin-left: auto;
  font-size: 13px;
  color: rgba(255,255,255,0.5);
  flex-shrink: 0;
}
.app-main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 24px;
  min-height: calc(100vh - 64px - 60px);
}
.app-footer {
  text-align: center;
  padding: 20px;
  color: #999;
  font-size: 13px;
  background: #f5f5f5;
}
</style>
