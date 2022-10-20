import { Map } from 'mapbox-gl'
import { baseUrl } from '@/store';

export function useGolfCourses(map: Map){
  console.log('use golf courses?', map)

  const addSource = ()=> {
    map.addSource('golf-courses', {
      type: 'geojson',
      // Use a URL for the value for the `data` property.
      data: `${baseUrl.value}/golf-courses?f=geojson`
    });
       
    map.addLayer({
      'id': 'golf-courses-layer',
      'type': 'circle',
      'source': 'golf-courses',
      'paint': {
        'circle-radius': 4,
        'circle-stroke-width': 2,
        'circle-color': 'red',
        'circle-stroke-color': 'white'
       }
    });

    //@ts-ignore
    window.map = map
  }

  // @ts-ignore
  if (map._loaded){
    addSource()
  } else {
    map.on('load', ()=> {
      console.log('map on load in gc?')
      addSource()
    })
  }

}