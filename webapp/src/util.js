export const CONSTANT = {
    DEFAULT_AUDIO_MOTION_OPTIONS : {
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
      }
}

export function getFormattedDate() {
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Jan is 0!
    const yyyy = today.getFullYear();

    const hour = String(today.getHours()).padStart(2, '0');
    const minutes = String(today.getMinutes()).padStart(2, '0');
    const seconds = String(today.getSeconds()).padStart(2, '0');

    const formattedDate = `${dd}:${mm}:${yyyy} ${hour}:${minutes}:${seconds}`;
    return formattedDate;
}

export function slugify(text) {
    return text.toString().toLowerCase()
        .replace(/\s+/g, '-')           // Replace spaces with -
        .replace(/[^\w-]+/g, '')        // Remove all non-word characters
        .replace(/--+/g, '-')           // Replace multiple - with single -
        .replace(/^-+/, '')             // Trim - from start of text
        .replace(/-+$/, '');            // Trim - from end of text
}

export function convertNewLinesToBR(text) {
    return text.replace(/\n/g, '<br>');
}