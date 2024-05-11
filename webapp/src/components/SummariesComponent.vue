<template>
    <div class="clip">
        <div class="row" @click="toggle">
            <div class="ten columns">
                <span @input="updateText" @keydown.enter.prevent @blur="postUpdate" contenteditable="true">{{
                    decodeURI(data.recording_name) }}</span>
            </div>
            <div class="two columns">
                <a class="u-pull-right">
                    <i class="icon si-chevron-right" v-show="!show"></i>
                    <i class="icon si-chevron-down" v-show="show"></i>
                </a>
            </div>
        </div>
        <div v-show="show">
            <div class="row">
                <div class="twelve columns">
                    <WaveSurfer :src="data.audio_file_name"></WaveSurfer>
                </div>
            </div>
            <div class="row">
                <div class="eight columns">
                    <div class="small-header">Full Transcript</div>
                    <p v-html="formatText(data.transcript)"></p>
                </div>
                <div class="four columns">
                    <div class="small-header">Summary</div>
                    <p v-if="data.summary.length" v-html="formatText(data.summary)"></p>
                    <div v-if="data.summary.length == 0">
                        <div>Summarization in progress</div>
                        <progress />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="four columns"><a :href="data.audio_file_name" title="Download"
                        :download="data.audio_file_name">
                        <i class="icon si-download"></i>
                    </a><a title="Delete" @click="confirmRemove">
                        <i class="icon si-trash"></i>
                    </a></div>
            </div>

        </div>
    </div>
</template>
<script>
import { removeSummary, updateRecordingName } from '@/api';
import WaveSurfer from './WaveSurfer';
export default {
    data() {
        return {
            show: false,
            editText: ''
        }
    },
    components: {
        WaveSurfer
    },
    props: {
        data: Object
    },
    methods: {
        confirmRemove() {
            const app = this;
            this.$confirm(
                {
                    message: 'Are you sure you want to delete this item?',
                    button: {
                        no: 'No',
                        yes: 'Yes'
                    },
                    /**
                    * Callback Function
                    * @param {Boolean} confirm
                    */
                    callback: async confirm => {
                        if (confirm) {
                            await app.remove()
                        }
                    }
                }
            )
        },
        postUpdate() {
            if (this.editText.trim().length) {
                updateRecordingName(encodeURI(this.editText), this.data.audio_file_name)
            }
        },
        updateText(event) {
            this.editText = event.target.innerText;
        },
        toggle() {
            this.show = !this.show;
        },
        formatText(text) {
            return text.replace(/\n/g, '<br>');
        },
        async remove() {
            await removeSummary(this.data.audio_file_name)
            this.emitter.emit('reload-soundclips');
        },
        createAudioWidget() {
            WaveSurfer.create({
                container: '#waveform',
                waveColor: '#4F4A85',
                progressColor: '#383351',
                url: '/audio.mp3',
            })
        }
    }
}
</script>
<style scoped>
.clip {
    padding: 12px 0px;
    text-align: left;
    border-bottom: 1px solid #E1E1E1;
}

.icon-small {
    font-size: 1em;
}
</style>