<template>
  <div class="container">
    <n-space vertical class="message-container" ref="messageContainer">
      <div v-for="message in messages" :key="message.message" class="message-bubble-container" :class="message.self ? 'own-message': 'bot-message'">
        {{message.message}}
      </div>
    </n-space>
    <div class="message-compose-container">
      <n-input v-model:value="currentMessage" @keyup.enter="sendMessage" size="large" type="text" placeholder="Write something..." />
      <n-button type="info" size="large" @click="sendMessage">Send</n-button>
    </div>
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
        {id: 3, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 4, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 5, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 6, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 7, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 8, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 9, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 10, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 11, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 12, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 13, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 14, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 15, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 16, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 17, self: false, message: "Eh, I'm hanging in there. How about you?"},
        {id: 18, self: true, message: "Can't complain either!"}
      ],
      currentMessage: null
    }
  },
  mounted() {
    this.scrollChatToBottom();
  },
  methods: {
    sendMessage() {
      if(this.currentMessage != null && this.currentMessage.trim() !== "") {
        let id = this.messages.length;
        this.messages.push({id: id, self: true, message: this.currentMessage});
        this.currentMessage = null;

        this.$nextTick(this.scrollChatToBottom);
      }
    },
    scrollChatToBottom() {
      this.$refs.messageContainer.$el.scrollTop = this.$refs.messageContainer.$el.scrollHeight;
    }
  }
}
</script>

<style scoped>
  .message-compose-container {
    display: flex;
    gap: 10px;
  }

  .container {
    display: flex;
    flex-direction: column;
    row-gap: 15px;
    width: 100%;
  }

  .message-container {
    overflow-y: scroll;
  }

  .message-bubble-container {
    padding: 10px;
    border-radius: 20px;
    font-size: 18px;
    margin-bottom: 8px;
    display: inline-block;
    max-width: 45%;
    overflow-wrap: break-word;
  }

  .bot-message {
    float: left;
    background-color: #3096bf;
  }

  .own-message {
    float: right;
    background-color: #57c441;
  }
</style>