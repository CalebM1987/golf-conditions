import { ref } from 'vue'
import {  GolfCourseFeature } from '@/types/golf';
import { Map, PointLike } from 'mapbox-gl'
import { useGolfCourses } from './golf-courses';
import { selectedIds, setWeatherLocation } from '@/store'
import { log } from '@/utils'

const didSetClickListener = ref(false)

export function useMapboxMap(map: Map){

  const { highlightPoints } = useGolfCourses(map)

  const addWeatherLayers = (layers: string[])=>{
    const CLIENT_ID = import.meta.env.VITE_AERIS_CLIENT_ID
    const CLIENT_SECRET = import.meta.env.VITE_AERIS_CLIENT_SECRET
    //@ts-ignore
    const account = new aerisweather.mapsgl.Account(CLIENT_ID, CLIENT_SECRET);

    //@ts-ignore
    const controller = new aerisweather.mapsgl.MapboxMapController(map, { account });
    
    setTimeout(()=> {
      layers.forEach((lyr)=> {
        controller.addWeatherLayer(lyr)
      }, 500)
    })
    
  }

  const onClick = (e: any)=> {
    // Set `bbox` as 5px reactangle area around clicked point.
    const bbox = [
      [e.point.x - 5, e.point.y - 5],
      [e.point.x + 5, e.point.y + 5]
    ] as [PointLike, PointLike]

    setWeatherLocation(e.lngLat.lng, e.lngLat.lat)

    // select features
    const selectedFeatures = map.queryRenderedFeatures(bbox, {
      layers: ['golf-courses-layer']
    });
    const ids = selectedFeatures.map(
      //@ts-ignore
      (feature: GolfCourseFeature) => feature.properties.id!
    );

    // Set a filter matching selected features by FIPS codes
    // to activate the 'counties-highlighted' layer.
    highlightPoints(ids);
    selectedIds.value = ids
  }

  const setMapClickListener = ()=> {
    if (!didSetClickListener.value){
      log('no map click listener set, adding now')
      map.on('click', onClick)
      didSetClickListener.value = true
    }
  }

  const removeMapClickListener = ()=> {
    if (didSetClickListener.value){
      log('removing map click listener')
      map.off('click', onClick)
      didSetClickListener.value = false
    }
  }

  setMapClickListener()

  return {
    map,
    addWeatherLayers,
    setMapClickListener,
    removeMapClickListener,
    didSetClickListener
  }
}