<template>
  <div class="wrapper">
    <chat-component></chat-component>
  </div>
</template>

<script>
import ChatComponent from './components/ChatComponent.vue'

export default {
  name: 'App',
  components: {
    ChatComponent
  }
}
</script>

<style>
.wrapper {
  max-width: 75%;
  margin: 15px auto 15px auto;
  max-height: 100vh;
  display: flex;
}

html, body {
  max-height: 100vh;
}
</style>
