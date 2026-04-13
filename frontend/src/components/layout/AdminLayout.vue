<template>
  <div class="admin-layout">
    <Sidebar />
    <div class="main-wrapper">
      <Header />
      <div class="content">
        <router-view />
      </div>
      <Footer />
    </div>
  </div>
</template>

<script setup>
import Sidebar from '../common/Sidebar.vue'
import Header from '../common/Header.vue'
import Footer from '../common/Footer.vue'
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.content {
  flex: 1;
  padding: 20px;
  background: #f0f2f5;
  overflow-y: auto;
}
</style>
