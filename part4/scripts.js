const API_URL = "http://127.0.0.1:5000"; // Change if your Flask runs elsewhere

// ---- Cookie helpers ----
function setCookie(name, value) {
  document.cookie = `${name}=${value}; path=/`;
}

function getCookie(name) {
  let cookies = document.cookie.split('; ');
  for (let cookie of cookies) {
    let [key, val] = cookie.split('=');
    if (key === name) return val;
  }
  return null;
}

// ---- LOGIN ----
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        setCookie("token", data.access_token);
        window.location.href = "index.html";
      } else {
        document.getElementById('login-error').innerText = "Invalid credentials";
      }
    });
  }
});

// ---- INDEX PAGE ----
document.addEventListener('DOMContentLoaded', () => {
  const placesList = document.getElementById('places-list');
  const loginLink = document.getElementById('login-link');
  const token = getCookie('token');

  if (placesList) {
    if (!token) {
      loginLink.style.display = "block";
    } else {
      loginLink.style.display = "none";
      fetchPlaces(token);
    }
  }

  async function fetchPlaces(token) {
    const res = await fetch(`${API_URL}/places`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) {
      const places = await res.json();
      displayPlaces(places);
    }
  }

  function displayPlaces(places) {
    placesList.innerHTML = "";
    places.forEach(place => {
      const card = document.createElement("div");
      card.classList.add("place-card");
      card.innerHTML = `
        <h3>${place.name}</h3>
        <p>Price: $${place.price_per_night}</p>
        <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
      `;
      placesList.appendChild(card);
    });
  }

  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', () => {
      const maxPrice = priceFilter.value;
      Array.from(document.getElementsByClassName('place-card')).forEach(card => {
        const price = parseInt(card.querySelector('p').innerText.replace("Price: $", ""));
        if (maxPrice === "all" || price <= parseInt(maxPrice)) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  }
});

// ---- PLACE DETAILS ----
document.addEventListener('DOMContentLoaded', () => {
  const placeDetails = document.getElementById('place-details');
  const token = getCookie('token');

  if (placeDetails) {
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("id");

    fetchPlaceDetails(token, placeId);
  }

  async function fetchPlaceDetails(token, placeId) {
    const res = await fetch(`${API_URL}/places/${placeId}`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) {
      const place = await res.json();
      displayPlaceDetails(place);
    }
  }

  function displayPlaceDetails(place) {
    placeDetails.innerHTML = `
      <div class="place-info">
        <h3>${place.name}</h3>
        <p>${place.description}</p>
        <p>Price: $${place.price_per_night}</p>
        <p>Host: ${place.host}</p>
        <p>Amenities: ${place.amenities.join(", ")}</p>
      </div>
      <h4>Reviews:</h4>
      ${place.reviews.map(r => `
        <div class="review-card">
          <p>${r.comment}</p>
          <small>By: ${r.user} - Rating: ${r.rating}</small>
        </div>
      `).join("")}
    `;

    if (token) {
      document.getElementById("add-review").style.display = "block";
    }
  }
});

// ---- ADD REVIEW ----
document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = getCookie('token');

  if (reviewForm) {
    if (!token) window.location.href = "index.html";

    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("id");

    reviewForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const reviewText = document.getElementById('review-text').value;

      const res = await fetch(`${API_URL}/places/${placeId}/reviews`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ comment: reviewText })
      });

      if (res.ok) {
        alert("Review submitted!");
        reviewForm.reset();
      } else {
        alert("Failed to submit review");
      }
    });
  }
});
