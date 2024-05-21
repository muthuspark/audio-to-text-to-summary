export const API = {
  GET_SUMMARIES: "/get_summaries",
  GET_SUMMARY: "/get_summary",
  REMOVE_SUMMARY: "/remove_summary",
  UPDATE_TITLE: "/update_title"
}

/**
 * Creates a payload object for a POST request.
 *
 * @param {Object|string} body The body of the request, which can be a stringified JSON or an object.
 * @returns {Object} The payload object containing the method, body, and headers for the POST request.
 */
export function payload(body) {
  const options = {
    method: 'POST', // Specify the method as POST
    headers: {
      'Content-Type': 'application/json' // Set the content type header
    },
    body: JSON.stringify(body) // Add the JSON data to the body
  };

  // Return the payload object
  return options;
}

export async function getSummaries() {
  try {
    const response = await fetch(API.GET_SUMMARIES, payload({}));
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

export async function getSummaryById(_id) {
  const response = await fetch(API.GET_SUMMARY, payload({ "id": _id }));

  // Check if response status is 404
  if (!response.ok) {
    const data = await response.json();
    // Handle 404 error
    throw new Error(data.message);
  }

  const data = await response.json();
  console.log(data);
  return data;
}


export async function removeSummary(audio_file_name) {

  try {
    const response = await fetch(API.REMOVE_SUMMARY, payload({
      "audio_file_name": audio_file_name
    }));
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

export async function updateRecordingName(recordingName, audioFileName) {
  try {
    const response = await fetch(API.UPDATE_TITLE, payload({
      "audio_file_name": audioFileName,
      "recording_name": recordingName
    }));
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}