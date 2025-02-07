let map;
        let markers = [];
        let userLat;
        let userLon;
      
        function initMap() {
          const defaultLocation = { lat: 20.5937, lng: 78.9629 }; // India's center coordinates
          map = new google.maps.Map(document.getElementById("map"), {
            zoom: 5,
            center: defaultLocation,
          });
          if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
              (position) => {
                userLat = position.coords.latitude; // Store user's latitude
                userLon = position.coords.longitude; // Store user's longitude
                const userLocation = {
                  lat: userLat,
                  lng: userLon,
                };
                console.log("Latitude:", userLat);
                console.log("Longitude:", userLon);
                map.setCenter(userLocation);
                map.setZoom(12); // Zoom in to user's location
              },
              () => {
                // Handle error when user denies permission
                handleLocationError(true, map.getCenter());
              },
              {
                enableHighAccuracy: true, // Enable high accuracy for better location
                timeout: 10000, // Timeout after 10 seconds
                maximumAge: 0, // Do not use cached position
            }
            );
          } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, map.getCenter());
          } 
        }
      
        function handleLocationError(browserHasGeolocation, pos) {
          const infoWindow = new google.maps.InfoWindow();
          infoWindow.setPosition(pos);
          infoWindow.setContent(
            browserHasGeolocation
              ? "Error: The Geolocation service failed."
              : "Error: Your browser doesn't support geolocation."
          );
          infoWindow.open(map);
        }
      

        function uploadAndDetectPlant() {
          const imageInput = document.getElementById("imageInput");
          const formData = new FormData();
          formData.append("image", imageInput.files[0]);
          
          // Add user's latitude and longitude
          formData.append('latitude', userLat);
          formData.append('longitude', userLon);
      
          // Get the progress bar element
          const progressBar = document.querySelector('.progress-bar');
          
          progressBar.style.width = "0%";
          progressBar.setAttribute("aria-valuenow", 0);
          progressBar.classList.remove('bg-success', 'bg-danger'); 
      
          // Create a new XMLHttpRequest for tracking upload progress
          const xhr = new XMLHttpRequest();
      
          // Update progress bar during upload
          xhr.upload.addEventListener("progress", function (e) {
              if (e.lengthComputable) {
                  const percentComplete = Math.round((e.loaded / e.total) * 100);
                  progressBar.style.width = percentComplete + "%";
                  progressBar.setAttribute("aria-valuenow", percentComplete);
              }
          });
      
          // On successful upload, complete the progress bar and handle fetch logic
          xhr.addEventListener("load", function () {
              if (xhr.status === 200) {
                  // Upload is complete
                  progressBar.style.width = "100%";
                  progressBar.classList.add('bg-success');
      
                  console.log("Latitude:", userLat, "Longitude:", userLon);
                  
                  // Once upload completes, detect plant species
                  fetch("/detect_plant_species", {
                      method: "POST",
                      body: formData,
                  })
                  .then((response) => response.json())
                  .then((data) => {
                      const treeSpecies = data.tree_species;
                      const weather = data.weather;
                      const soil = data.soil;
      
                      // Use user location from initMap and detected data to add a marker
                      addMarker(userLat, userLon, treeSpecies, weather, soil);
                  })
                  .catch((error) => {
                      console.error("Error during plant detection:", error);
                  });
              } else {
                  console.error("Upload failed");
                  progressBar.classList.add('bg-danger');
              }
          });
      
          // Handle any errors during the upload
          xhr.addEventListener("error", function () {
              progressBar.classList.add('bg-danger');
              console.error("Error uploading the file.");
          });
      
          // Initialize the upload request
          xhr.open("POST", "/detect_plant_species");
          xhr.send(formData);
      }
      
      
        function addMarker(lat, lon, treeSpecies, weather, soil) {
          const position = { lat: lat, lng: lon };
          const marker = new google.maps.Marker({
            position: position,
            map: map,
          });
          markers.push(marker);
          map.setCenter(position);
          map.setZoom(12);
      
          // Create an info window using the data fetched from the backend
          const infoWindowContent = `
            <div class="info-content">
                <h3>Tree Species: ${treeSpecies}</h3>
                ${
                  weather
                    ? `<p>Temperature: ${weather.temperature}°C</p>
                        <p>Humidity: ${weather.humidity}%</p>
                        <p>Wind Speed: ${weather.wind_speed} km/h</p>
                        <p>Visibility: ${weather.visibility} m</p>`
                    : ""
                }
                ${soil ? `<p>Soil Type: ${soil.soil_type}</p>` : ""}
            </div>
          `;
          const infoWindow = new google.maps.InfoWindow({
            content: infoWindowContent,
          });
      
          marker.addListener("click", () => {
            infoWindow.open({
              anchor: marker,
              map,
              shouldFocus: false,
            });
          });
        }