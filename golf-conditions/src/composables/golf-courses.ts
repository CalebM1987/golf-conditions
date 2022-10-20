import { GolfCourseFeature } from './../types/golf';
import { ref } from 'vue'
import { Map } from 'mapbox-gl'
import { getGolfCourses } from '@/services';
import { baseUrl, golfCourses } from '@/store';
import { log } from '@/utils'

const didAddLayers = ref(false)

export function useGolfCourses(map: Map){

  const addSource = async ()=> {

    const { data } = await getGolfCourses({f: 'geojson'})

    log(`loaded ${data.features?.length ?? 0} golf courses`)

    //@ts-ignore
    golfCourses.value = data.features ?? [] as unknown as GolfCourseFeature[]

    map.addSource('golf-courses', {
      type: 'geojson',
      // @ts-ignore
      data
      
    });
       
    map.addLayer({
      'id': 'golf-courses-layer',
      'type': 'symbol',
      'source': 'golf-courses',
      'layout': {
        'text-field': ['get', 'CourseName'],
        'text-variable-anchor': ['top', 'bottom', 'left', 'right'],
        'text-radial-offset': 0.5,
        'text-justify': 'auto',
        'icon-image': 'golf-15',
        'icon-size': 1,
        'text-size': {
          "stops": [
              [0, 0],
              [9, 0],
              [10, 11]
            ]
          }
        },
        paint: {
          'text-halo-color': 'white',
          'text-halo-width': 1,
          'text-color': 'green',
        }
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

    didAddLayers.value = true
    
  }

  if (!didAddLayers.value){
    // @ts-ignore
    if (map._loaded){
      addSource()
    } else {
      map.on('load', ()=> {
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