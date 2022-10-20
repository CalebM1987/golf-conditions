import { GolfCourseFeature } from './../types/golf';
import { ref } from 'vue'
import { Map } from 'mapbox-gl'
import { getGolfCourses } from '@/services';
import { baseUrl, golfCourses } from '@/store';

const didAddLayers = ref(false)

export function useGolfCourses(map: Map){
  console.log('use golf courses?', map)

  const addSource = async ()=> {

    const { data } = await getGolfCourses({f: 'geojson'})

    console.log(`loaded ${data.features?.length ?? 0} golf courses`)

    //@ts-ignore
    golfCourses.value = data.features ?? [] as unknown as GolfCourseFeature[]

    map.addSource('golf-courses', {
      type: 'geojson',
      // @ts-ignore
      data
      // Use a URL for the value for the `data` property.
      // data: `${baseUrl.value}/golf-courses?f=geojson`
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
       },
      //  'layout': {
      //     'text-field': ['get', 'CourseName'],
      //     'text-variable-anchor': ['top', 'bottom', 'left', 'right'],
      //     'text-radial-offset': 0.5,
      //     'text-justify': 'auto',
      //     // 'icon-image': ['get', 'icon']
      //   }
    });

    map.addLayer({
      'id': 'golf-courses-highlighted',
      'type': 'circle',
      'source': 'golf-courses',
      'paint': {
        'circle-radius': 8,
        'circle-stroke-width': 2,
        'circle-color': 'cyan',
        'circle-stroke-color': 'white'
       },
       'filter': ['in', 'id', '']
    })

    //@ts-ignore
    window.map = map

    didAddLayers.value = true
    
  }

  if (!didAddLayers.value){
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

  const highlightPoints = (ids: number[]) => {
    map.setFilter('golf-courses-highlighted', ['in', 'id', ...ids])
  }

  const clearHighlightedPoints = ()=> map.setFilter('golf-courses-highlighted', ['in', 'id', ''])

  return {
    map,
    highlightPoints,
    clearHighlightedPoints
  }

}