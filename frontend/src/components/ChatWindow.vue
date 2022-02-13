<template>
  <div class="container">
    <n-scrollbar ref="scrollbarRef">
      <div class="message-container" ref="messageContainer">
        <transition-group name="expand">
          <template v-for="message in messages" :key="message.id" >
            <chat-bubble :message="message" class="message-bubble-container"></chat-bubble>
          </template>
        </transition-group>
      </div>
    </n-scrollbar>
    <div class="message-compose-container">
      <n-input v-model:value="currentMessage" @keyup.enter="sendMessage" size="large" type="text"
               placeholder="Write something..."/>
      <Icon size="35" color="black" @click="sendMessage" class="sendIcon">
        <Send/>
      </Icon>
    </div>
  </div>
</template>

<script>
import {Send} from '@vicons/ionicons5'
import {Icon} from '@vicons/utils'
import ChatBubble from "@/components/ChatBubble";
import { v4 as uuidv4 } from 'uuid';

export default {
  name: "ChatWindow",
  components: {
    Icon,
    Send,
    ChatBubble
  },
  data() {
    return {
      messages: [
        // {id: 1, self: true, message: "Hey! How many cases have there been in Austria this today?"},
        // {
        //   id: 2,
        //   self: false,
        //   message: "I'm afraid I don't have any data on COVID cases in Austria today, yet. :( Try " +
        //       "again a bit later."
        // },
        // {id: 3, self: true, message: "How many people have been vaccinated this week in Germany?"},
        // {id: 4, self: false, message: "More than **500.000** people have been vaccinated this week in Germany."},
        // {id: 5, self: true, message: "On which day where most people vaccinated in Austria?"},
        // {id: 6, self: false, message: "**26th of September 2021** was the day were the most people were vaccinated in Austria."},

      ],
      currentMessage: null
    }
  },
  mounted() {
    this.addWelcomeMessage()
  },
  methods: {
    addMessage(self, message, loading) {
      var id = uuidv4();
      this.messages.push({
        id: id,
        self: self,
        message: message,
        loading: loading
      })

      return id;
    },
    addWelcomeMessage() {
      var message = "Hi there! My name is **Covbot**, I am a chatbot that can help you answer certain questions about COVID." +
          "\n\n\nIn particular, I have access to information about:\n" +
          "1. The number of positive COVID cases detected in certain countries every day.\n" +
          "2. The number of vaccinations that were administered in certain countries every day.\n\n" +
          "I was built as part of a project for a bachelor thesis. I'm still in my infancy, meaning that I have a couple " +
          "of limitations:\n" +
          "1. Unfortunately, I don't have any memory (yet). :( This means that every message you send" +
          " has to contain all of the information that is necessary for me, you can't refer to anything that you've" +
          " written in the past.\n" +
          "2. I'm kind of bad at small talk and understanding difficult questions. So try to keep your questions " +
          "relatively short and precise!\n\n" +
          "Anyway, ask away! ;)"

      var messageId = this.addMessage(false, message, true);

      setTimeout(() => {
        this.messages.filter(msg => msg.id === messageId)[0].loading = false;
      }, 2000)
    },
    sendMessage() {
      if (this.currentMessage != null && this.currentMessage.trim() !== "") {
        this.addMessage(true, this.currentMessage, false)
        this.currentMessage = null;

        // Simulate response
        let id = this.addMessage(false, "I successfully received your message. This will be the answer!", true);

        setTimeout(() => {
          this.messages.filter(msg => msg.id === id)[0].loading = false;
          this.$nextTick(this.scrollChatToBottom)
        }, 2000)

        this.$nextTick(this.scrollChatToBottom);
      }
    },
    scrollChatToBottom() {
      this.$refs.scrollbarRef.scrollTo({top: this.$refs.messageContainer.scrollHeight})
    }
  }
}
</script>

<style>

.message-compose-container {
  display: flex;
  justify-content: space-around;
  gap: 10px;
  margin: 13px;
  padding: 10px;
  border-radius: 10px;
  background-color: white;
  box-shadow: 0 0 10px 1px rgba(0, 0, 0, 0.2);
}

.container {
  display: flex;
  flex-direction: column;
  background-color: #F2F6FC;
  border-radius: 12px;
  width: 100%;
}

.sendIcon {
  margin: 0 5px 0 5px;
  cursor: pointer;
}

.message-container {
  padding: 15px 15px 0 15px;
  overflow-y: auto;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.sendButton {
  border-radius: 10px;
}

.message-bubble-container {
  padding: 14px 17px 14px 17px;
  flex: 0 0 100%;
  border-radius: 20px;
  font-size: 18px;
  max-width: 60%;
  overflow-wrap: break-word;
  box-shadow: 0 0 10px 1px rgba(0, 0, 0, 0.2);
  margin-top: 10px;
  margin-bottom: 10px;
}

.expand-enter-active {
  animation: bounce-in 0.3s;
}

.expand-leave-active {
  animation: bounce-in 0.3s reverse;
}

@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  100% {
    transform: scale(1);
  }
}
</style>