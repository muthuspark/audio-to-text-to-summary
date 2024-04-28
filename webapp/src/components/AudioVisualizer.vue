<template>
  <div class="visualizationContainer" ref="visualizationContainer"></div>
</template>
<script>
import AudioMotionAnalyzer from 'audiomotion-analyzer';

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

      audioMotion.setOptions({
        mode: 10,
        bgAlpha: .7,
        fillAlpha: .6,
        gradient: 'steelblue',
        lineWidth: 2,
        lumiBars: false,
        maxFreq: 16000,
        radial: false,
        reflexAlpha: 1,
        linearAmplitude: true,
        linearBoost: 1.5,
        reflexBright: 1,
        reflexRatio: .5,
        showScaleX: false,
        showBgColor: false,
        roundBars: true,
        showPeaks: false,
        moothing: 0.8,
        overlay: true
      });
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