export function getSummaries() {
    return new Promise((resolve, reject) => {
        fetch('/get_summaries', { method: 'POST' })
          .then(response => response.json())
          .then(data => {
            console.log(data);
            resolve(data);
          })
          .catch(error => {
            console.error('Error:', error);
            reject(error);
          });
      });
}

export function removeSummary(audio_file_name) {

  const raw = JSON.stringify({
    "audio_file_name": audio_file_name
  });

  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  return new Promise((resolve, reject) => {
      fetch('/remove_summary', { method: 'POST', body: raw, headers: myHeaders, })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          resolve(data);
        })
        .catch(error => {
          console.error('Error:', error);
          reject(error);
        });
    });
}