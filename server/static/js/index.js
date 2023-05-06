function updateValue() {
  fetch('/inout').then(response => response.json())
             .then(data => {
               const inElement = document.getElementById('in');
               const outElement = document.getElementById('out');
               const attendanceElement = document.getElementById('attendance');
               inElement.innerHTML = data["in"];
               outElement.innerHTML = data["out"];
               attendanceElement.innerHTML = data["in"] - data["out"];
             });
}

function updateTemperature() {
  fetch('/temp').then(res => res.json())
    .then(temp => {
    const tempElement = document.getElementById('temp');
    tempElement.innerHTML = temp + '°C';
  })
}

setInterval(updateValue, 1000); // Update every second
setInterval(updateTemperature, 10000);
