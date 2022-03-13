<template>
  <n-dialog-provider>
    <div className="wrapper">
      <chat-window></chat-window>
    </div>
  </n-dialog-provider>
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
  margin: auto;
  max-height: 100vh;
  display: flex;
}

@media only screen and (min-width: 750px) {
  .wrapper {
    max-width: 75%;
  }
}

@media only screen and (min-width: 1300px) {
  .wrapper {
    max-width: 55%;
  }
}


html {
  height: 100vh;
}

body {
  height: calc(100vh - 2 * 15px);
  padding: 15px 0 15px 0;
}

#app, .wrapper {
  height: 100%;
}
</style>
