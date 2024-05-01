<template>
    <div class="clip">
        <section>
            {{ data.recording_name }}
        </section>
        <section>
            <audio controls="true" :src="data.audio_file_name"></audio>
        </section>
        <div class="grid">
            <div>
                <details>
                    <summary role="button" class="secondary">Summary</summary>
                    {{ data.summary }}
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
export default {
    props: {
        data: Object
    },
    methods: {
    }
}
</script>