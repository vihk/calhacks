<template>

  <form @submit.prevent="submit">
    <input v-model="textInput">  
    <button>Submit</button>
  </form>

  <div>Response: {{ response }}</div>

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

    // Create JSON object 
    const body = {
      text: this.textInput
    }

    // Stringify it 
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