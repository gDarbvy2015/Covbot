<template>
  <div class="wrapper">
    <chat-window></chat-window>
  </div>
</template>

<script>
import ChatWindow from './components/ChatWindow.vue'

export default {
  name: 'App',
  components: {
    ChatWindow
  }
}
</script>

<style>
.wrapper {
  max-width: 55%;
  margin: auto;
  max-height: 100vh;
  display: flex;
}

html{
  height: 100vh;
}

body {
  height: calc(100vh - 2*15px);
  padding: 15px 0 15px 0;
}

#app, .wrapper {
  height: 100%;
}
</style>
