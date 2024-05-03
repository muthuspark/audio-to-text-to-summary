<template>
    <div class="clip">
        <section>
            <nav>
                <ul>
                    <li><strong>{{ data.recording_name }}</strong></li>
                </ul>
                <ul>
                    <li><audio controls="true" :src="data.audio_file_name"></audio></li>
                </ul>
                <ul>
                    <li><button title="Download" class="contrast">
                            <a :href="data.audio_file_name" :download="data.audio_file_name">
                                Download
                            </a>
                        </button></li>
                    <li><button title="Delete" class="contrast" @click="remove">
                            Delete
                        </button></li>
                </ul>
            </nav>
        </section>
        <div class="grid">
            <div>
                <details>
                    <summary role="button" class="secondary">Summary</summary>
                    <div v-if="data.summary.length">{{ data.summary }}</div>
                    <div v-if="data.summary.length == 0">
                        <div>Summarization in progress</div>
                        <progress />
                    </div>
                </details>
            </div>
            <div>
                <details>
                    <summary role="button" class="secondary">Full Transcript</summary>
                    {{ data.transcript }}
                </details>
            </div>
        </div>
        <hr>
    </div>
</template>
<script>
import { removeSummary } from '@/api';

export default {
    props: {
        data: Object
    },
    methods: {
        async remove() {
            await removeSummary(this.data.audio_file_name)
            this.emitter.emit('reload-soundclips');
        }
    }
}
</script>