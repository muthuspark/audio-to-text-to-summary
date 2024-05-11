<template>
  <div class="visualizationContainer" ref="visualizationContainer"></div>
</template>
<script>
import AudioMotionAnalyzer from 'audiomotion-analyzer';
import { CONSTANT } from '@/util';
export default {
  props: {
    stream: Object
  },
  methods: {
    buildVisualizer() {
      if (!this.audioCtx) {
        this.audioCtx = new AudioContext();
      }
      const audioMotion = new AudioMotionAnalyzer(
        this.$refs.visualizationContainer,
        {
          source: this.audioCtx.createMediaStreamSource(this.stream)
        }
      );

      audioMotion.setOptions(CONSTANT.DEFAULT_AUDIO_MOTION_OPTIONS);
    }
  }, 
  mounted() {
    this.buildVisualizer();
  }
};
</script>
<style>
.visualizationContainer {
    height: 8em;
}

.visualizationContainer canvas {
    border-radius: 12px;
}
</style>