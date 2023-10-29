<template>
  <div class="container">
    <form @submit.prevent="submit" class="form">
      <input v-model="textInput" class="input-field">
      <button class="submit-button">Submit</button>
    </form>
    <div class="response">
      <div v-for="(segment, index) in formattedResponseSegments" :key="index" class="response-box">
        <p class="response-title">{{ segment[0] }}</p>
        <ul class="response-list">
          <li v-for="(item, itemIndex) in segment.slice(1)" :key="itemIndex">{{ item }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      textInput: '',
      response: null,
    };
  },
  computed: {
    formattedResponseSegments() {
      if (this.response && this.response.result) {
        const result = this.response.result;
        let segments = [];
        for (const key in result) {
          const subObject = result[key];
          let segment = [key];
          for (const subKey in subObject) {
            segment.push(`${subKey}: ${subObject[subKey]}`);
          }
          segments.push(segment);
        }
        return segments;
      }
      return [];
    },
  },
  methods: {
    async submit() {
      const body = {
        text: this.textInput,
      };

      const jsonBody = JSON.stringify(body);

      const response = await fetch('http://localhost:3000', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonBody,
      });

      this.response = await response.json();
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #333; /* Dark gray background */
}

.form {
  text-align: center;
}

.input-field {
  width: 300px;
  padding: 10px;
  margin: 10px;
  background-color: #000; /* Black input field */
  color: #fff; /* White text color */
  border: none;
  border-radius: 5px;
}

.submit-button {
  padding: 10px 20px;
  background-color: #0074cc; /* Beautiful blue submit button */
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.response {
  margin-top: 20px;
  color: #000000; /* White text color for the response */
}

.response-box {
  background-color: #fff;
  padding: 10px;
  margin: 10px;
  border-radius: 5px;
}

.response-title {
  font-weight: bold;
  text-decoration: underline;
  font-size: 16px;
}

.response-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.response-list li {
  font-size: 14px;
}
</style>
