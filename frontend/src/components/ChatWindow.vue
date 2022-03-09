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
               placeholder="Write something..." :disabled="!consent" />
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
import {useDialog} from "naive-ui";

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
      ],
      currentMessage: null,
      consent: null
    }
  },
  mounted() {
    if(localStorage.getItem("information_consent") === null) {
      this.askConsent();
    } else {
      this.consent = JSON.parse(localStorage.getItem("information_consent"));
      if(this.consent) {
        this.addWelcomeMessage();
      }
    }

  },
  methods: {
    askConsent() {
      if(localStorage.getItem("information_consent") == null) {
        const dialog = useDialog()
        dialog.create({
          title: 'Note',
          content: 'All of the messages sent here are stored on the server and might be used ' +
              'to improve the chatbot, so please don\'t enter any private information.',
          positiveText: 'Okay',
          closable: false,
          onPositiveClick: () => {
            localStorage.setItem("information_consent", "true");
            this.setConsent(true);
            this.addWelcomeMessage();
          },
        })
      }
    },
    setConsent(value) {
      this.consent = value;
    },
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
          "1. The number of positive COVID cases detected in a certain country on a certain day.\n" +
          "2. The number of vaccinations that were administered in a certain country on a certain day.\n" +
          "3. The number of people that were vaccinated in a certain country on a certain day.\n\n" +
          "I was built as part of a bachelor thesis. If you are curious about how I work, you can check out my " +
          "[source code](https://github.com/LaurenzV/Covbot) if you want.\n\n" +
          "I'm still in my infancy, so expect that I that there might be errors and I might not be able to understand " +
          "all of your questions. In particular, keep in mind that:\n" +
          "1. Unfortunately, I don't have a memory. :( This means that every message you send" +
          " has to contain all of the information that is necessary for me, you can't refer to anything that you've" +
          " written before.\n" +
          "2. I'm kind of bad at small talk and understanding complex questions. So try to keep your questions " +
          "relatively short and precise!\n\n" +
          "With that said, ask away!"

      var messageId = this.addMessage(false, message, true);

      setTimeout(() => {
        this.messages.filter(msg => msg.id === messageId)[0].loading = false;
      }, 1500)
    },
    sendMessage() {
      if (this.currentMessage != null && this.currentMessage.trim() !== "") {
        this.addMessage(true, this.currentMessage, false);

        let id = this.addMessage(false, "", true);
        let messageContent = ""
        this.axios.get("http://127.0.0.1:5000/", {params: {msg: this.currentMessage}}).then((response) => {
          messageContent = response.data.msg
        }).catch((error) => {
          if (error.response) {
            messageContent = "Whoops, looks like an error occurred while processing your request... It has been taken " +
                "note of, try asking a different question in the meanwhile!"
          } else if (error.request) {
            messageContent = "It looks like the server is down, so I can't process your request... Please notify the " +
                "adminstrator.";
          } else {
            messageContent = "Sorry, an unknown error occurred...";
          }
        }).finally(() => {
          let msg = this.messages.filter(msg => msg.id === id)[0];
          msg.message = messageContent;
          msg.loading = false;
          this.$nextTick(this.scrollChatToBottom)
        });

        this.currentMessage = null
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