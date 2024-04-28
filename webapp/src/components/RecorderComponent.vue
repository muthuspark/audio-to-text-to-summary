<template>
  <div class="wrapper">
    <section class="main-controls">
      <div class="main-controls-content">
        <AudioVisualizer :stream="stream" v-if="stream"></AudioVisualizer>
        <div class="btncontainer">
          <div id="buttons">
            <div v-show="!recording" ><button class="record" @click="record"><div class="circle" ></div></button><span>Record</span></div>
            <div v-show="recording" ><button class="stop" @click="stop"><div class="square" ></div></button><span>Stop</span></div>
          </div>
          <StopWatch ref="stopWatch"></StopWatch>
        </div>
      </div>
    </section>
    <section class="sound-clips">
      <SoundClip v-for="(clip, index) in audioClips" :name="clip.name" :source="clip.source" :blob="clip.blob" :key="index"></SoundClip>
    </section>
  </div>
</template>
<script>
import AudioVisualizer from './AudioVisualizer.vue'
import StopWatch from './StopWatch.vue'
import SoundClip from './SoundClip.vue'
export default {
  name: 'RecorderComponent',
  components: {
    AudioVisualizer,
    StopWatch,
    SoundClip
, },
  data() {
    return {
      stream: null,
      recording: false,
      mediaRecorder: null,
      audioClips: []
    } 
  },
  methods: {
    getFormattedDate() {
      const today = new Date();
      const dd = String(today.getDate()).padStart(2, '0');
      const mm = String(today.getMonth() + 1).padStart(2, '0'); // Jan is 0!
      const yyyy = today.getFullYear();

      const hour = String(today.getHours()).padStart(2, '0');
      const minutes = String(today.getMinutes()).padStart(2, '0');
      const seconds = String(today.getSeconds()).padStart(2, '0');

      const formattedDate = `${dd}:${mm}:${yyyy} ${hour}:${minutes}:${seconds}`;
      return formattedDate;
    },
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
            app.audioClips.push({
              'name': `Recording - ${app.getFormattedDate()}`,
              'source': window.URL.createObjectURL(blob),
              'download': `Recording - ${app.getFormattedDate()}.wav`,
              'blob':blob
            });
            
            console.log("recorder stopped");

            /*clipLabel.onclick = function () {
              const existingName = clipLabel.textContent;
              const newClipName = prompt("Enter a new name for your sound clip?");
              if (newClipName === null) {
                clipLabel.textContent = existingName;
              } else {
                clipLabel.textContent = newClipName;
              }
            };

            const formData = new FormData();
            formData.append('audio', blob, `${clipLabel.textContent}.wav`);

            fetch('/upload', {
              method: 'POST',
              body: formData
            })
            .then(response => {
              if (response.ok) {
                console.log('Audio uploaded successfully');
              } else {
                console.error('Audio upload failed');
              }
            })
            .catch(error => {
              console.error('Error uploading audio:', error);
            });
*/
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
