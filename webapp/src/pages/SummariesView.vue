<template>
    <div class="clip" v-if="data">
        <div class="row">
            <div class="eight columns">
                <h5>
                    <span>{{ decodeURI(data.recording_name) }}</span>
                </h5>
            </div>
            <div class="four columns right"><a :href="data.audio_file_name" title="Download"
                    :download="data.audio_file_name">
                    <i class="icon si-download"></i>
                </a><a title="Delete" @click="confirmRemove">
                    <i class="icon si-trash"></i>
                </a></div>
        </div>

        <div class="row">
            <div class="twelve columns">
                <WaveSurfer :src="data.audio_file_name"></WaveSurfer>
            </div>
        </div>
        <div class="row">
            <div class="eight columns">
                <div class="small-header">Full Transcript</div>
                <p v-html="convertNewLinesToBR(data.transcript)"></p>
            </div>
            <div class="four columns">
                <div class="small-header">Summary</div>
                <p v-if="data.summary.length" v-html="convertNewLinesToBR(data.summary)"></p>
                <div v-if="data.summary.length == 0">
                    <div>Summarization in progress</div>
                    <progress />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { removeSummary, getSummaryById } from '@/api';
import { convertNewLinesToBR } from '@/util'

import WaveSurfer from '@/components/WaveSurfer.vue';

export default {
    data() {
        return {
            convertNewLinesToBR,
            show: false,
            editText: '',
            data: null
        }
    },
    components: {
        WaveSurfer
    },
    props: {
        id: String
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
                            app.$toast.success("Summary deleted", { duration: 2000 });
                            location.href = "/"
                        }
                    }
                }
            )
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
    },
    async mounted() {
        try{
            this.data = await getSummaryById(this.$route.params.id);
        }catch(e){
            this.$toast.error(e.message, { duration: 2000 });
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

.right {
    text-align: right;
}
</style>