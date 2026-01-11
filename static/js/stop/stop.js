let map = L.map("map").setView([33.8806, -5.5238], 16);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

let stopMarkers = [],
  stops = [],
  selectedStopId = null,
  contextMenu = document.getElementById("contextMenu"),
  selectedMarker = null;
let chosenLocation = null;
let tempMarker = null;

function createMarker(lat, lng, name, id = null) {
  const customIcon = L.icon({
    iconUrl: "static/images/station1.png",
    iconRetinaUrl: "static/images/station1.png",
    iconSize: [30, 45],
    iconAnchor: [15, 45],
    popupAnchor: [0, -40],
    tooltipAnchor: [0, -35],
  });
  const marker = L.marker([lat, lng], {
    draggable: true,
    icon: customIcon,
  }).addTo(map);
  marker
    .bindTooltip(`<b>${name}</b>`, {
      permanent: true,
      direction: "top",
      className: "custom-stop-tooltip",
    })
    .openTooltip();
  marker.stopId = id;

  marker.on("dragend", async () => {
    const { lat, lng } = marker.getLatLng();
    if (marker.stopId) {
      await fetch(`/update_stop/${marker.stopId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          stop_name: name,
          location: { type: "Point", coordinates: [lat, lng] },
        }),
      });
    }
  });

  marker.on("contextmenu", (e) => {
    selectedMarker = marker;
    contextMenu.innerHTML = `
            <div onclick="deleteMarker()">Delete Stop</div>
          `;
    contextMenu.style.left = `${e.originalEvent.pageX}px`;
    contextMenu.style.top = `${e.originalEvent.pageY}px`;
    contextMenu.style.display = "block";
  });

  stopMarkers.push(marker);
  return marker;
}

map.on("click", () => (contextMenu.style.display = "none"));

map.on("click", (e) => {
  if (tempMarker) {
    map.removeLayer(tempMarker);
  }
  chosenLocation = e.latlng;

  tempMarker = L.marker(chosenLocation).addTo(map);
});

async function addStop() {
  const name = document.getElementById("stopName").value.trim();
  if (!chosenLocation) {
    return alert("Please select a location on the map first by clicking.");
  }
  if (!name) {
    return alert("Enter a stop name.");
  }

  const lat = chosenLocation.lat;
  const lng = chosenLocation.lng;

  const res = await fetch("/add_stop", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, location: [lat, lng] }),
  });
  const data = await res.json();

  createMarker(lat, lng, name, data._id);

  // Eingaben und temporäre Markierung löschen
  document.getElementById("stopName").value = "";
  if (tempMarker) {
    map.removeLayer(tempMarker);
    tempMarker = null;
  }
  chosenLocation = null;

  fetchStops();
}

async function fetchStops() {
  const res = await fetch("/get_stops");
  const data = await res.json();
  stops = data;
  const dropdown = document.getElementById("stopsDropdown");
  dropdown.innerHTML = '<option value="">Select a stop</option>';
  data.forEach((stop) => {
    const option = document.createElement("option");
    option.value = stop._id;
    option.textContent = stop.stop_name;
    dropdown.appendChild(option);
  });
  clearMap();
  data.forEach((stop) =>
    createMarker(
      stop.location.coordinates[0],
      stop.location.coordinates[1],
      stop.stop_name,
      stop._id
    )
  );
}

function focusOnStop(id) {
  const stop = stops.find((s) => s._id === id);
  if (stop) {
    map.setView([stop.lat, stop.lng], 18);
  }
}

function deleteMarker() {
  if (!selectedMarker) return;
  const id = selectedMarker.stopId;
  if (id && confirm("Delete this stop?")) {
    fetch(`/delete_stop/${id}`, { method: "DELETE" }).then(() => {
      map.removeLayer(selectedMarker);
      fetchStops();
      contextMenu.style.display = "none";
      selectedMarker = null;
    });
  }
}

function clearMap() {
  stopMarkers.forEach((m) => map.removeLayer(m));
  stopMarkers = [];
  selectedStopId = null;
}

function deleteSelectedStop() {
  const id = document.getElementById("stopsDropdown").value;
  if (!id || !confirm("Delete selected stop?")) return;
  fetch(`/delete_stop/${id}`, { method: "DELETE" }).then(() => {
    fetchStops();
  });
}

fetchStops();
