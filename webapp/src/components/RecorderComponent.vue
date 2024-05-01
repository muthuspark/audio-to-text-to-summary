<template>
  <section>
      <article>
        <header>
          <AudioVisualizer :stream="stream" v-if="stream"></AudioVisualizer>
        </header>
        <div v-show="!recording">
          <button class="record" @click="record">
            <span>Record</span>
          </button>
        </div>
        <div v-show="recording">
          <button class="stop" @click="stop">
            <span>Stop</span>
          </button>
        </div>
        <footer>
          <StopWatch ref="stopWatch"></StopWatch>
        </footer>
      </article>
  </section>
  <section>
    <article>
      <header>Current Recordings</header>
      <SoundClip v-for="(clip, index) in audioClips" :data="clip" :key="index"></SoundClip>
    </article>
  </section>
  <section>
    <article>
      <header>Summaries</header>
      <SummariesComponent v-for="(clip, index) in summarizedRecordings" :data="clip" :key="index"></SummariesComponent>
    </article>
  </section>
</template>
<script>
import AudioVisualizer from './AudioVisualizer.vue'
import StopWatch from './StopWatch.vue'
import SoundClip from './SoundClip.vue'
import SummariesComponent from './SummariesComponent.vue'
import { getFormattedDate } from '../util'
export default {
  name: 'RecorderComponent',
  components: {
    AudioVisualizer,
    StopWatch,
    SoundClip,
    SummariesComponent
  },
  data() {
    return {
      stream: null,
      recording: false,
      mediaRecorder: null,
      audioClips: [],
      summarizedRecordings: []
    }
  },
  methods: {
    initEvents() {
      this.emitter.on('recording-started', () => this.recording = true)
      this.emitter.on('recording-stopped', () => this.recording = false)
      this.emitter.on('reload-soundclips', () => this.getAllSummaries())
    },
    record() {
      this.emitter.emit('recording-started')
      this.mediaRecorder.start();
    },
    stop() {
      this.emitter.emit('recording-stopped')
      this.mediaRecorder.stop();
    },
    getAllSummaries() {
      const app = this;
      fetch('/get_summaries', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          app.summarizedRecordings = data;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  },
  mounted() {
    this.initEvents();
    this.getAllSummaries();
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
            'download': `Recording - ${name}.webm`,
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
