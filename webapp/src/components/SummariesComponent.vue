<template>
    <div class="clip">
        <div class="row" @click="toggle">
            <div class="ten columns">
                {{ data.recording_name }}
            </div>
            <div class="two columns">
                <a class="u-pull-right">
                    <i class="icon si-chevron-right" v-show="!show"></i>
                    <i class="icon si-chevron-down" v-show="show"></i>
                </a>
            </div>
            <!-- <div class="four columns"><a :href="data.audio_file_name" title="Download" vv class="u-pull-right"
                        :download="data.audio_file_name">
                        <i class="icon si-download"></i>
                    </a><a title="Delete" href="#" class="u-pull-right" @click="remove">
                        <i class="icon si-trash"></i>
                    </a></div> -->
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
                    <p v-html="formatTranscript(data.transcript)"></p>
                </div>
                <div class="four columns">
                    <div class="small-header">Summary</div>
                    <p v-if="data.summary.length">{{ data.summary }}</p>
                    <div v-if="data.summary.length == 0">
                        <div>Summarization in progress</div>
                        <progress />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { removeSummary } from '@/api';
import WaveSurfer from './WaveSurfer';

export default {
    data() {
        return {
            show: false
        }
    },
    components: {
        WaveSurfer
    },
    props: {
        data: Object
    },
    methods: {
        toggle() {
            this.show = !this.show;
        },
        formatTranscript(transcript) {
            let firstIndex = transcript.indexOf('SPEAKER');
            if (firstIndex !== -1) {
                // Find subsequent occurrences starting from the position after the first occurrence
                let subsequentOccurrences = transcript.slice(firstIndex + 'SPEAKER'.length).replace(/SPEAKER/g, '<br><br>SPEAKER');
                // Concatenate the transcript with the modified subsequent occurrences
                return transcript.slice(0, firstIndex) + 'SPEAKER' + subsequentOccurrences;
            }
            return transcript;
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
</style>