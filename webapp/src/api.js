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