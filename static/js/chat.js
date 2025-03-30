const chatArea = document.getElementById('chat');
fetchPosts();

function setCookie(name, value, days) { 
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function addPost(event) {   
    event.preventDefault();

    createPost();
}

// make post request to add a post to the server
async function createPost() {
    const postContent = document.getElementById('post-text-input').value.trim();

    if (postContent) {
        try {
            const response = await fetch('/add-post', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 'text': postContent }) //put many shit inside
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

        } catch (error) {
            console.log(error);
            return;
        }

        // Refresh comments after adding
        fetchPosts();

    } else {
        console.log("please enter text");
    }

}



// Fetch comments from the server
async function fetchPosts() {
    var response
    try {
        response = await fetch('/get-posts');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`); //await dont reject http errors like 404 or 500, so we need this line
        }
    } catch (error) {
        console.log(error);
        return
    }

    const dataFromDatabase = await response.json(); 

    clearChatArea();
    for (var lineData of dataFromDatabase.posts) {
        createPostElement(lineData.post_id, lineData.content, lineData.created_at);
    }
}


// make a post element and add it to the chat area
function createPostElement(post_id, postContent, timestamp) { 
    const newPost = document.createElement('div');
    newPost.className = 'post';

    const postIdElement = document.createElement('div');
    postIdElement.className = 'post-id';
    postIdElement.textContent = post_id;

    const postContentElement = document.createElement('p');
    postContentElement.textContent = postContent; // Use textContent to prevent XSS

    const timestampElement = document.createElement('span');
    timestampElement.className = 'timestamp';
    console.log(timestamp);
    timestampElement.textContent = timestamp; // Use textContent to prevent XSS

    newPost.appendChild(postIdElement);
    newPost.appendChild(postContentElement);
    newPost.appendChild(timestampElement);

    const chatArea = document.getElementById('chat'); // Ensure chatArea is defined
    chatArea.appendChild(newPost);
    document.getElementById('post-text-input').value = '';
}

function clearChatArea() {
    chatArea.innerHTML = '';
}