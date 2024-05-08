<template>
  <div class="container">
    <nav class="navbar">
      <div class="container">
        <ul class="navbar-list">
          <li class="navbar-item"><a class="navbar-link" href="#"><strong>Speech Synopsis</strong></a></li>
        </ul>
      </div>
    </nav>
    <RecorderComponent/>
  </div>
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