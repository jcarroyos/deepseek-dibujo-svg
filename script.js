document.addEventListener('DOMContentLoaded', () => {
    const gallery = document.getElementById('gallery');
    const images = ['gatos/gato_20250502_191301.svg',
                    'gatos/gato_20250502_192038.svg',
                    'gatos/gato_20250502_195255.svg',
  
        
    ]; // Lista local de imágenes

    images.forEach(image => {
        const imgElement = document.createElement('img');
        imgElement.src = image;
        imgElement.alt = 'Imagen de gato';
        gallery.appendChild(imgElement);
    });
});