<template>
    <div class="time-display">{{ formattedTime }}</div>
</template>
<script>
export default {
  data() {
    return {
      elapsedTime: 0,
      isRunning: false,
      intervalId: null
    } 
  },
  computed: {
    formattedTime() {
      const seconds = Math.floor(this.elapsedTime / 1000) % 60;
      const minutes = Math.floor(this.elapsedTime / (1000 * 60)) % 60;
      const hours = Math.floor(this.elapsedTime / (1000 * 60 * 60));
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    },
  },
  methods: {
    start() {
      if (this.isRunning) {
        clearInterval(this.intervalId);
      } else {
        this.intervalId = setInterval(() => {
          this.elapsedTime += 10;
        }, 10);
      }
      this.isRunning = !this.isRunning;
    },
    reset() {
      clearInterval(this.intervalId);
      this.elapsedTime = 0;
      this.isRunning = false;
    },
  },
  mounted() {
    this.emitter.on('recording-started', () => {
      this.start();
    })

    this.emitter.on('recording-stopped', () => {
      this.reset();
    })
  }
}

</script>