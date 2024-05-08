<template>
  <div >
    <div class="docs-section">
      <article>
        <header>
          <AudioVisualizer :stream="stream" v-show="stream"></AudioVisualizer>
        </header>
        <div class="recording-actions">
          <div v-show="!recording">
            <button class="button-primary" @click="record" :disabled="!recordingSupported">
              <span>Record</span>
            </button>
          </div>
          <div v-show="recording">
            <button class="button-primary" @click="stop">
              <span>Stop</span>
            </button>
          </div>
          <small id="invalid-helper" v-if="!recordingSupported">
            MediaDevices recording not supported on your browser!
          </small>
        </div>
        <footer class="center">
          <StopWatch ref="stopWatch"></StopWatch>
        </footer>
      </article>
    </div>
    <div class="docs-section" v-if="audioClips.length">
      <h6 class="docs-header">Summarization in progress</h6>
      <SoundClip v-for="(clip, index) in audioClips" :data="clip" :key="index"></SoundClip>
    </div>
    <div class="docs-section">
      <h6 class="docs-header">Summaries</h6>
      <SummariesComponent v-for="(clip, index) in summarizedRecordings" :data="clip" :key="index">
      </SummariesComponent>
    </div>
  </div>
</template>
<script>
import AudioVisualizer from './AudioVisualizer.vue'
import StopWatch from './StopWatch.vue'
import SoundClip from './SoundClip.vue'
import SummariesComponent from './SummariesComponent.vue'
import { getFormattedDate } from '@/util'
import { getSummaries } from '@/api'
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
      unsupported: true,
      recordingSupported: false,
      mediaRecorder: null,
      audioClips: [],
      summarizedRecordings: [],
      chunks: []
    }
  },
  methods: {
    initEvents() {
      this.emitter.on('recording-started', () => this.recording = true)
      this.emitter.on('recording-stopped', () => this.recording = false)
      this.emitter.on('reload-soundclips', this.summaries)
    },
    mediaRecorderOnStop({ data }) {
      console.log("Last data to read (after MediaRecorder.stop() called).", data);
      const blob = new Blob(this.chunks, { type: this.mediaRecorder.mimeType });
      this.chunks = [];
      const name = getFormattedDate();
      this.audioClips.push({
        name: `Recording - ${name}`,
        source: window.URL.createObjectURL(blob),
        download: `Recording - ${name}.webm`,
        blob,
      });
      console.log("recorder stopped");
    },
    mediaRecorderOndataavailable({ data }) {
      this.chunks.push(data);
    },
    async getUserMediaOnSuccess(stream) {
      try {
        this.mediaRecorder = new MediaRecorder(stream);
        this.stream = stream;
        this.mediaRecorder.onstop = this.mediaRecorderOnStop;
        this.mediaRecorder.ondataavailable = this.mediaRecorderOndataavailable;
        await this.mediaRecorder.start();
      } catch (error) {
        console.error('Error starting MediaRecorder:', error);
      }
    },
    async record() {
      this.emitter.emit('recording-started');
      const constraints = { audio: true };
      try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        await this.getUserMediaOnSuccess(stream);
      } catch (error) {
        console.error('Error getting user media:', error);
      }
    },
    stop() {
      this.emitter.emit('recording-stopped')
      this.mediaRecorder.stop();
      this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
    },
    async summaries() {
      this.summarizedRecordings = await getSummaries()
    }
  },
  mounted() {
    this.summaries();
    if (navigator.mediaDevices.getUserMedia) {
      this.recordingSupported = true;
      this.initEvents();
      console.log("The mediaDevices.getUserMedia() method is supported.");
    } else {
      console.log("MediaDevices.getUserMedia() not supported on your browser!");
    }
  }
}
</script>
