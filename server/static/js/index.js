function updateValue() {
  fetch('/inout').then(response => response.json())
             .then(data => {
               const inElement = document.getElementById('in');
               const outElement = document.getElementById('out');
               inElement.innerHTML = data["in"];
               outElement.innerHTML = data["out"];
             });
}

function updateTemperature() {
  fetch('/temp').then(res => res.json())
    .then(temp => {
    const tempElement = document.getElementById('temp');
    tempElement.innerHTML = temp + '°C';
  })
}

setInterval(updateValue, 1000);
setInterval(updateTemperature, 10000);
