<template>
    <div class="clip">
        <p class="audioname">{{ name }}</p>
        <audio controls="true" :src="source"></audio>
        <button title="Summarize" class="icons" @click="summarize">
            <img src="../assets/summary.png">
        </button>
        <button title="Download" class="icons">
            <a :href="source" :download="source">
                <img src="../assets/download.png">
            </a>
        </button>
        <button title="Delete" class="icons" @click="remove">
            <img src="../assets/delete.png">
        </button>
    </div>
</template>
<script>
export default {
    props: {
        source: String,
        name: String,
        blob: Object
    },
    methods: {
        remove(e) {
            e.target.closest(".clip").remove();
        },
        summarize() {
            const formData = new FormData();
            formData.append('audio', this.blob, `${this.name}.wav`);
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
        }
    }
}
</script>