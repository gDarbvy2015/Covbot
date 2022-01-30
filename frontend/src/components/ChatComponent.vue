<template>
  <n-space vertical style="margin-bottom: 10px">
    <div v-for="message in messages" :key="message.message" class="message-container" :class="{'own-message': message.self}">
      {{message.message}}
    </div>
  </n-space>
  <div class="container">
    <n-input v-model:value="value" size="large" type="text" placeholder="Write something..." />
    <n-button type="info" size="large">Send</n-button>
  </div>
</template>

<script>
export default {
  name: "ChatComponent",
  data() {
    return {
      messages: [
        {id: 1, self: true, message: "Hey! How's it going?"},
        {id: 2, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 3, self: true, message: "Can't complain either!"}
      ],
      value: null
    }
  }
}
</script>

<style scoped>
  .container {
    display: flex;
    gap: 10px;
  }

  .message-container {
    padding: 10px;
    border-radius: 20px;
    font-size: 16px;
    display: inline-block;
    background-color: #57c441;
  }

  .own-message {
    float: right;
  }
</style>