self.addEventListener('install', function(event) {
  console.log('Service Worker installing.');
});

self.addEventListener('fetch', function(event) {
  // You can add offline support here
});
