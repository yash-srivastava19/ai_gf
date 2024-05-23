document.addEventListener('DOMContentLoaded', () => {
    const inputField = document.getElementById('input-field');
    const submitButton = document.getElementById('submit-button');
    const videoContainer = document.getElementById('video-container');
    const staticImage = document.getElementById('avatar');

    staticImage.style.display = 'block';
    
    submitButton.addEventListener('click', async () => {
      const input = inputField.value.trim();
      if (input) {
        try {  
          const response = await fetch('/get-video-from-chat', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input }),
          });
  
          if (response.ok) {
            const data = await response.json();
            const videoUrl = data.video_url;
            if (videoUrl) {
              staticImage.style.display = 'none';
              videoContainer.innerHTML = `<video src="${videoUrl}" controls></video>`;
            } else {
              videoContainer.innerHTML = '<p>No video found for the given input.</p>';
            }
          } else {
            videoContainer.innerHTML = '<p>Error occurred while fetching the video.</p>';
          }
        } catch (error) {
          console.error('Error:', error);
          videoContainer.innerHTML = '<p>Error occurred while fetching the video.</p>';
        }
      }
    });
  });