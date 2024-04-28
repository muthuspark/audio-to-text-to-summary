<template>
  <div class="wrapper">
    <section class="main-controls">
      <div class="main-controls-content">
        <AudioVisualizer :stream="stream" v-if="stream"></AudioVisualizer>
        <div class="btncontainer">
          <div id="buttons">
            <div v-show="!recording"><button class="record" @click="record">
                <div class="circle"></div>
              </button><span>Record</span></div>
            <div v-show="recording"><button class="stop" @click="stop">
                <div class="square"></div>
              </button><span>Stop</span></div>
          </div>
          <StopWatch ref="stopWatch"></StopWatch>
        </div>
      </div>
    </section>
    <section class="sound-clips">
      <SoundClip v-for="(clip, index) in audioClips" :name="clip.name" :source="clip.source" :blob="clip.blob"
        :key="index"></SoundClip>
    </section>
  </div>
</template>
<script>
import AudioVisualizer from './AudioVisualizer.vue'
import StopWatch from './StopWatch.vue'
import SoundClip from './SoundClip.vue'
import { getFormattedDate } from '../util'
export default {
  name: 'RecorderComponent',
  components: {
    AudioVisualizer,
    StopWatch,
    SoundClip
    ,
  },
  data() {
    return {
      stream: null,
      recording: false,
      mediaRecorder: null,
      audioClips: []
    }
  },
  methods: {
    initEvents() {
      this.emitter.on('recording-started', () => this.recording = true)
      this.emitter.on('recording-stopped', () => this.recording = false)
    },
    record() {
      this.emitter.emit('recording-started')
      this.mediaRecorder.start();
    },
    stop() {
      this.emitter.emit('recording-stopped')
      this.mediaRecorder.stop();
    }
  },
  mounted() {
    this.initEvents();
    const app = this;
    // Main block for doing the audio recording
    if (navigator.mediaDevices.getUserMedia) {
      console.log("The mediaDevices.getUserMedia() method is supported.");

      const constraints = { audio: true };
      let chunks = [];

      let onSuccess = function (stream) {
        app.mediaRecorder = new MediaRecorder(stream);
        app.stream = stream;

        app.mediaRecorder.onstop = function (e) {
          console.log("Last data to read (after MediaRecorder.stop() called).", e);
          const blob = new Blob(chunks, { type: app.mediaRecorder.mimeType });
          chunks = [];
          const name = getFormattedDate();
          app.audioClips.push({
            'name': `Recording - ${name}`,
            'source': window.URL.createObjectURL(blob),
            'download': `Recording - ${name}.wav`,
            'blob': blob
          });
          console.log("recorder stopped");
        };

        app.mediaRecorder.ondataavailable = function (e) {
          chunks.push(e.data);
        };
      };

      let onError = function (err) {
        console.log("The following error occured: " + err);
      };

      navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);
    } else {
      console.log("MediaDevices.getUserMedia() not supported on your browser!");
    }
  }
}
</script>
