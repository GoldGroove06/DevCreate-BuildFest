// State management
let selectedFile = null;
let loading = false;

// DOM elements
const videoInput = document.getElementById('video-input');
const uploadBtn = document.getElementById('upload-btn');
const uploadContent = document.getElementById('upload-content');
const loadingSection = document.getElementById('loading-section');
const outputSection = document.getElementById('output-section');
const outputVideo = document.getElementById('output-video');
const videoSource = document.getElementById('video-source');
const toastContainer = document.getElementById('toast-container');

// Event listeners
videoInput.addEventListener('change', (e) => {
    selectedFile = e.target.files[0] || null;
});

uploadBtn.addEventListener('click', handleUpload);

// Toast function
function showToast(message, duration = 3000) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('fade-out');
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    }, duration);
}

// Handle file upload
async function handleUpload() {
    if (!selectedFile) {
        showToast('Please select a file');
        return;
    }
    
    setLoading(true);
    
    const formData = new FormData();
    formData.append('video', selectedFile);
    
    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        console.log(data);
        
        // Display output video
        videoSource.src = data.url;
        outputVideo.load();
        outputSection.style.display = 'block';
        
        showToast('Upload successful!');
    } catch (error) {
        console.error('Upload error:', error);
        showToast('Upload failed. Please try again.');
    } finally {
        setLoading(false);
    }
}

// Toggle loading state
function setLoading(isLoading) {
    loading = isLoading;
    if (isLoading) {
        uploadContent.style.display = 'none';
        loadingSection.style.display = 'block';
    } else {
        uploadContent.style.display = 'flex';
        loadingSection.style.display = 'none';
    }
}
