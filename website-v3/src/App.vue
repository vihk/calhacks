<template>
  <!-- form -->
  
  <p>Response: {{ response }}</p>

</template>

<script>
export default {

  data() {
    return {
      response: null
    }
  },

  methods: {
    async onSubmit(text) {
      const response = await fetch('/some/api', {
        method: 'POST',
        body: text  
      })  
      
      this.response = await response.json()
    }
  }
}
</script>