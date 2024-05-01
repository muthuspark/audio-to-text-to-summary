<template>
    <div class="clip">
        <nav>
            <ul>
                <li><strong>{{ data.name }}</strong></li>
            </ul>
            <ul>
                <li><audio controls="true" :src="data.source"></audio></li>
            </ul>
            <ul>
                <li><button title="Summarize" class="contrast" @click="summarize">
                        Summarize
                    </button></li>
                <li><button title="Download" class="contrast">
                        <a :href="data.source" :download="data.source">
                            Download
                        </a>
                    </button></li>
                <li><button title="Delete" class="contrast" @click="remove">
                        Delete
                    </button></li>
            </ul>
        </nav>
        <progress v-if="summarizing" />
        <hr>
    </div>
</template>
<script>
export default {
    data() {
        return {
            summarizing: false,
        }
    },
    props: {
        data: Object
    },
    methods: {
        checkIfSummaryCompleted(recordingName) {
            this.summarizing = true;
            const app = this;
            const raw = JSON.stringify({
                "recording_name": recordingName
            });
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };
            const clrInterval = setInterval(function () {
                fetch('/summarizing_completed', requestOptions)
                    .then(response => {
                        if (response.ok) {
                            clearInterval(clrInterval);
                            app.summarizing = false;
                            app.emitter.emit('reload-soundclips');
                        }
                    })
                    .catch(error => {
                        console.error('Error uploading audio:', error);
                    });
            }, 5000);
        },
        remove(e) {
            e.target.closest(".clip").remove();
        },
        summarize() {
            const app = this;
            const formData = new FormData();
            formData.append('audio', this.data.blob, `${this.data.name}.webm`);
            formData.append('name', this.data.name);
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
                .then(response => {
                    console.log(response);
                    app.checkIfSummaryCompleted(app.data.name);
                })
                .catch(error => {
                    console.error('Error uploading audio:', error);
                });
        }
    }
}
</script>