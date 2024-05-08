<template>
    <div></div>
</template>

<script>
import WaveSurfer from "wavesurfer.js";
export default {
    props: ['src'],
    data() {
        return {
            waveSurfer: {},
            options: {
                waveColor: '#33C3F0',
                progressColor: '#014C75',
                /** Stretch the waveform to fill the container, true by default */
                fillParent: true,
                /** Whether to show default audio element controls */
                mediaControls: true,
                /** Allow to drag the cursor to seek to a new position */
                dragToSeek: false,
                /** Hide the scrollbar */
                hideScrollbar: false,
            }
        };
    },
    mounted() {
        let options = this.options;
        options['url'] = this.src;
        let wsOptions = Object.assign({ container: this.$el }, options);
        this.waveSurfer = WaveSurfer.create(wsOptions);
    }
};
</script>

<style lang="css" scoped>
div {
    position: relative;
}
</style>