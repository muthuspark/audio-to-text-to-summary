<template>
  <header><h1>SpeechSynopsis</h1></header>
  <main class="container-fluid" >
    <RecorderComponent/>
  </main>
</template>
<script>
import RecorderComponent from './components/RecorderComponent.vue'

export default {
  name: 'App',
  components: {
    RecorderComponent
  }
}
</script>