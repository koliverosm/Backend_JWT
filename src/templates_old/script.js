const fotoElement = document.getElementById('foto');
const nombreElement = document.getElementById('nombre');

// Hacer una petición GET
fetch('http://127.0.0.1:5000/uploads/getfoto')
  .then(response => {
    fotoElement.src = 'data:image/jpeg;base64,' + response;
   console.log(response);
  })
  .then(data => {
    // Actualizar la foto y el nombre
    fotoElement.src = 'data:image/jpeg;base64,' + data; // Suponiendo que la foto está en formato base64
  
  })
  .catch(error => console.error('Error:', error));
