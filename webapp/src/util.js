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