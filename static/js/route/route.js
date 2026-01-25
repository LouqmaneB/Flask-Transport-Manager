const map = L.map("map").setView([33.8806, -5.5238], 16);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

let markers = [];
let points = [];
let selectedRouteId = null;
let routingControl = null;

const contextMenu = document.getElementById("contextMenu");
let selectedMarker = null;
const stopIdToCoordinates = {};
const stopsMarkers = [];

async function fetchStops() {
  const res = await fetch("/admin_api/get_stops");
  const response = await res.json();

  const stops = response.data.stopsWithRoutes;

  stops.forEach((item) => {
    const stop = item.stop;
    const lat = stop.location.coordinates[0];
    const lng = stop.location.coordinates[1];
    stopIdToCoordinates[stop.id] = { lat, lng };

    const marker = L.marker([lat, lng], {
      title: stop.stop_name,
      icon: L.icon({
        iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
        iconSize: [25, 25],
        iconAnchor: [12, 24],
        popupAnchor: [0, -20],
      }),
    })
      .addTo(map)
      .bindPopup(stop.stop_name);
    marker.on("click", () => {
      const order = points.length + 1;
      points.push({ stopId: stop.id, order });
      const routeMarker = createMarker(lat, lng);
      routeMarker.stopId = stop.id;
      markers.push(routeMarker);
      updateRoute();
      if (selectedRouteId) updateRouteInDB();
      console.log(points);
    });

    stopsMarkers.push(marker);
  });
}

function createMarker(lat, lng) {
  const marker = L.marker([lat, lng], { draggable: true }).addTo(map);
  marker.dragging.disable();

  marker.on("contextmenu", (e) => {
    selectedMarker = marker;
    contextMenu.innerHTML = `<div onclick="deleteMarker()">Delete Point</div>`;
    contextMenu.style.left = `${e.originalEvent.pageX}px`;
    contextMenu.style.top = `${e.originalEvent.pageY}px`;
    contextMenu.style.display = "block";
  });

  return marker;
}

map.on("click", () => {
  contextMenu.style.display = "none";
});

function deleteMarker() {
  if (!selectedMarker) return;
  map.removeLayer(selectedMarker);
  markers = markers.filter((m) => m !== selectedMarker);
  points = points.filter((p) => p.stopId !== selectedMarker.stopId);
  selectedMarker = null;
  contextMenu.style.display = "none";
  updateRoute();
  if (selectedRouteId) updateRouteInDB();
}

function updateRoute() {
  if (routingControl) {
    map.removeControl(routingControl);
  }

  console.log(points);
  if (points.length < 2) return;

  const waypoints = points
    .map((p) => stopIdToCoordinates[p.stopId])
    .filter(Boolean)
    .map((coord) => L.latLng(coord.lat, coord.lng));

  routingControl = L.Routing.control({
    waypoints,
    routeWhileDragging: false,
    addWaypoints: false,
    draggableWaypoints: false,
    show: false,
    createMarker: () => null,
  }).addTo(map);
}

async function saveRoute() {
  const name = document.getElementById("routeName").value.trim();
  if (!name || !points.length) return alert("Provide name and points");

  await fetch("/admin_api/save_route", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, points }),
  });

  document.getElementById("routeName").value = "";
  clearMap();
  fetchRoutes();
}

async function fetchRoutes() {
  const res = await fetch("/admin_api/get_routes");
  const routes = await res.json();
  const dropdown = document.getElementById("routesDropdown");

  dropdown.innerHTML = `<option value="">Select a route</option>`;
  routes.data.forEach((route) => {
    const option = document.createElement("option");
    option.value = route._id;
    option.textContent = route.routeName;
    dropdown.appendChild(option);
  });

  if (selectedRouteId) {
    dropdown.value = selectedRouteId;
  }
}

async function loadRoute(id) {
  if (!id) return;
  const res = await fetch(`/admin_api/get_route/${id}`);
  const route = await res.json();
  if (!route || !route.data) return;

  clearMap();
  selectedRouteId = id;

  route.data.stops
    .sort((a, b) => a.order - b.order)
    .forEach((p) => {
      const stop = p.stopId; // stopId is actually the stop object
      const coord = stopIdToCoordinates[stop.id]; // use stop.id here
      if (!coord) return;

      const marker = createMarker(coord.lat, coord.lng);
      marker.stopId = stop.id;
      markers.push(marker);

      points.push({ stopId: stop.id, order: p.order });
    });

  updateRoute();
}

async function deleteSelectedRoute() {
  const id = document.getElementById("routesDropdown").value;
  if (!id || !confirm("Delete selected route?")) return;

  await fetch(`/admin_api/delete_route/${id}`, { method: "DELETE" });
  clearMap();
  fetchRoutes();
}

async function updateRouteInDB() {
  if (!selectedRouteId) return;
  await fetch(`/admin_api/update_route/${selectedRouteId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ stops: points }),
  });
}

function clearMap() {
  markers.forEach((m) => map.removeLayer(m));
  markers = [];
  points = [];
  selectedRouteId = null;

  if (routingControl) {
    map.removeControl(routingControl);
    routingControl = null;
  }

  contextMenu.style.display = "none";
}

// Anfangsbelastung
fetchStops();
fetchRoutes();
