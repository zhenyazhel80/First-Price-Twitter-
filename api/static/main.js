// ----------------- USERS ----------------- 
async function loadUsers() {
  const response = await fetch('http://127.0.0.1:8000/users/');
  const users = await response.json();

  // Dropdown for posting tweet
  const select = document.getElementById('userSelect');
  select.innerHTML = '';
  users.forEach(user => {
    const option = document.createElement('option');
    option.value = user.id;
    option.textContent = user.username;
    select.appendChild(option);
  });

  // List of users
  const userList = document.getElementById('userList');
  userList.innerHTML = '';
  users.forEach(user => {
    const li = document.createElement('li');
    li.textContent = `ID: ${user.id} | Username: ${user.username} | Email: ${user.email}`;
    userList.appendChild(li);
  });
}

// Create Account
document.getElementById('createUserForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('newUsername').value;
  const email = document.getElementById('newEmail').value;
  const password = document.getElementById('newPassword').value;

  const response = await fetch('http://127.0.0.1:8000/users/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });

  const msg = document.getElementById('createUserMessage');
  if (response.ok) {
    msg.textContent = 'Account created successfully!';
    loadUsers();
  } else {
    const error = await response.json();
    msg.textContent = error.detail || 'Failed to create account.';
  }
});

// ----------------- LOGIN -----------------
document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('loginUsername').value;
  const password = document.getElementById('loginPassword').value;

  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  try {
    const response = await fetch('http://127.0.0.1:8000/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData
    });

    const data = await response.json();
    const msg = document.getElementById('loginMessage');

    if (response.ok) {
      msg.textContent = `Welcome, ${data.username}`;
      localStorage.setItem('loggedInUserId', data.user_id);
    } else {
      msg.textContent = data.detail || 'Login failed.';
    }
  } catch (err) {
    console.error('Login error:', err);
    document.getElementById('loginMessage').textContent = 'Something went wrong.';
  }
});

// ----------------- TWEETS -----------------
async function loadTweets() {
  const response = await fetch('http://127.0.0.1:8000/tweets/');
  const tweets = await response.json();
  displayTweets(tweets.reverse());
}

document.getElementById('tweetForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const userId = document.getElementById('userSelect').value;
  const content = document.getElementById('content').value;

  if (!userId || !content.trim()) {
    alert("Select a user and write a tweet!");
    return;
  }

  await fetch(`http://127.0.0.1:8000/tweets/?user_id=${userId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content })
  });

  document.getElementById('content').value = '';
  loadTweets();
});

function displayTweets(tweets) {
  const list = document.getElementById("tweet-list");
  list.innerHTML = "";

  tweets.forEach(tweet => {
    const item = document.createElement("li");
    item.className = "tweet-item";

    const contentSpan = document.createElement("span");
    contentSpan.innerHTML = `User ${tweet.owner_id}: ${highlightHashtags(tweet.content)}`;
    item.appendChild(contentSpan);

    // Edit
    const editBtn = document.createElement("button");
    editBtn.textContent = "✏️";
    editBtn.onclick = () => {
      const newContent = prompt("Edit tweet:", tweet.content);
      if (newContent !== null) {
        fetch(`/tweets/${tweet.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: newContent })
        }).then(res => {
          if (res.ok) loadTweets();
          else alert("Failed to update tweet.");
        });
      }
    };
    item.appendChild(editBtn);

    // Delete
    const delBtn = document.createElement("button");
    delBtn.textContent = "🗑️";
    delBtn.onclick = () => {
      if (confirm("Are you sure you want to delete this tweet?")) {
        fetch(`/tweets/${tweet.id}`, { method: "DELETE" }).then(res => {
          if (res.ok) loadTweets();
          else alert("Failed to delete tweet.");
        });
      }
    };
    item.appendChild(delBtn);

    // Likes count
    const likeCount = document.createElement("span");
    likeCount.textContent = ` ❤️ ${tweet.likes || 0} `;
    item.appendChild(likeCount);

    // Like button
    const likeBtn = document.createElement("button");
    likeBtn.textContent = "👍";
    likeBtn.onclick = async () => {
      const userId = localStorage.getItem('loggedInUserId');
      if (!userId) {
        alert("Please log in to like tweets.");
        return;
      }

      const res = await fetch(`/likes/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: parseInt(userId), tweet_id: tweet.id })
      });

      if (res.ok) {
        loadTweets();
      } else {
        const error = await res.json();
        alert("Failed to like tweet: " + (error.detail || "Unknown error"));
      }
    };
    item.appendChild(likeBtn);

    list.appendChild(item);
  });
}

// ----------------- SEARCH -----------------
async function searchTweets() {
  const query = document.getElementById('searchInput').value;
  if (!query.trim()) return alert("Please enter a search term.");

  const response = await fetch(`http://127.0.0.1:8000/tweets/search/?q=${encodeURIComponent(query)}`);
  const tweets = await response.json();
  displayTweets(tweets);
}

async function searchHashtags() {
  const tag = document.getElementById('hashtagInput').value;
  if (!tag.trim()) return alert("Please enter a hashtag.");

  const response = await fetch(`http://127.0.0.1:8000/hashtags/search/?tag=${encodeURIComponent(tag)}`);
  const tweets = await response.json();
  displayTweets(tweets);
}

// Hashtag Highlighter
function highlightHashtags(text) {
  return text.replace(/(#\w+)/g, '<span style="color: blue;">$1</span>');
}

// ----------------- USER SEARCH -----------------
async function searchAccounts() {
  const query = document.getElementById("searchUsername").value.trim();
  const list = document.getElementById("searchResults");

  if (!query) {
    alert("Please enter a username.");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/users/search/?username=${encodeURIComponent(query)}`);
    const results = await response.json();

    list.innerHTML = ""; // Clear previous results

    if (results.length === 0) {
      list.innerHTML = "<li>No users found.</li>";
      return;
    }

    results.forEach(user => {
      const li = document.createElement("li");
      li.textContent = `ID: ${user.id} | Username: ${user.username} | Email: ${user.email}`;
      list.appendChild(li);
    });
  } catch (err) {
    console.error("Error searching users:", err);
    list.innerHTML = "<li>Error searching users.</li>";
  }
}

// ----------------- INITIAL LOAD -----------------
loadUsers();
loadTweets();
