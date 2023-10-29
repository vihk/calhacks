<template>
  <div class="container">
    <form @submit.prevent="submit" class="form">
      <input v-model="textInput" class="input-field">
      <button class="submit-button">Submit</button>
    </form>

    <div class="response">Response: {{ response }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      textInput: '',
      response: null
    }
  },

  methods: {
    async submit() {
      const body = {
        text: this.textInput
      }

      const jsonBody = JSON.stringify(body)

      const response = await fetch('http://localhost:3000', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: jsonBody
      })

      this.response = await response.json()
    }
  }
}
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
  color: #fff; /* White text color for the response */
}
</style>