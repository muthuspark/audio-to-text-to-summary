<template>
  <div class="wrapper">
    <section class="main-controls">
      <div class="main-controls-content">
        <div class="container" id="container"></div>
        <div class="btncontainer">
          <div id="buttons">
            <button class="record"><div class="circle" ></div></button>
            <button class="stop"><div class="square" ></div></button>
          </div>
          <div class="time-display"><span v-show="isRunning" >{{ formattedTime }}</span></div>
        </div>
      </div>
    </section>
    <section class="sound-clips">
    </section>
  </div>
</template>
<script>
import AudioMotionAnalyzer from 'audiomotion-analyzer';
import downloadIcon from '../assets/download.png';
import deleteIcon from '../assets/delete.png';
const icons = {
  'download' : downloadIcon,
  'delete' : deleteIcon
}
export default {
  name: 'RecorderComponent',
  data() {
    return {
      elapsedTime: 0,
      isRunning: false,
      intervalId: null,
      icons: icons
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
    startStop() {
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
    getIcon(name) {
      const img = document.createElement('img');
      img.src = this.icons[name];
      return img;
    }
  },
  mounted() {
      // Set up basic variables for app
      const record = document.querySelector(".record");
      const stop = document.querySelector(".stop");
      const soundClips = document.querySelector(".sound-clips");

      // Disable stop button while not recording
      stop.disabled = true;
      stop.style.display = "none";

      let audioCtx;

      const app = this;
      // Main block for doing the audio recording
      if (navigator.mediaDevices.getUserMedia) {
        console.log("The mediaDevices.getUserMedia() method is supported.");

        const constraints = { audio: true };
        let chunks = [];

        let onSuccess = function (stream) {
          const mediaRecorder = new MediaRecorder(stream);

          // visualize(stream);
          if (!audioCtx) {
            audioCtx = new AudioContext();
          }
          const audioMotion = new AudioMotionAnalyzer(
            document.getElementById('container'),
            {
              source: audioCtx.createMediaStreamSource(stream)
            }
          );

          audioMotion.setOptions(  {
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
          } );

          record.onclick = function () {
            mediaRecorder.start();
            app.reset();
            app.startStop();
            console.log(mediaRecorder.state);
            console.log("Recorder started.");
            record.style.display = "none";
            stop.style.display = "flex";

            stop.disabled = false;
            record.disabled = true;
          };

          stop.onclick = function () {
            mediaRecorder.stop();
            app.startStop();
            console.log(mediaRecorder.state);
            console.log("Recorder stopped.");
            record.style.display = "flex";
            stop.style.display = "none";

            stop.disabled = true;
            record.disabled = false;
          };

          mediaRecorder.onstop = function (e) {
            console.log("Last data to read (after MediaRecorder.stop() called).", e);

            const clipContainer = document.createElement("div");
            const clipLabel = document.createElement("p");
            clipLabel.className = "audioname";
            const audio = document.createElement("audio");
            const deleteButton = document.createElement("button");
            deleteButton.className = "icons";
            const downloadButton = document.createElement("button");
            const downloadLink = document.createElement("a");
            downloadButton.appendChild(downloadLink);
            downloadButton.className = "icons";

            clipContainer.classList.add("clip");
            audio.setAttribute("controls", "");

            downloadLink.appendChild(app.getIcon("download"));
            deleteButton.appendChild(app.getIcon("delete"));

            clipLabel.textContent = `Recording - ${app.getFormattedDate()}`;

            clipContainer.appendChild(clipLabel);
            clipContainer.appendChild(audio);
            clipContainer.appendChild(downloadButton);
            clipContainer.appendChild(deleteButton);
            soundClips.appendChild(clipContainer);

            audio.controls = true;
            const blob = new Blob(chunks, { type: mediaRecorder.mimeType });
            
            chunks = [];
            const audioURL = window.URL.createObjectURL(blob);
            audio.src = audioURL;

            downloadLink.href = audioURL;
            downloadLink.download = `${clipLabel.textContent}.wav`;
            
            console.log("recorder stopped");

            deleteButton.onclick = function (e) {
              e.target.closest(".clip").remove();
            };

            clipLabel.onclick = function () {
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

          };

          mediaRecorder.ondataavailable = function (e) {
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
