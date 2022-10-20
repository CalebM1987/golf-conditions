<script lang="ts" setup>
import { ref } from 'vue'
import { Map } from 'mapbox-gl'
import { MapboxMap } from 'vue-mapbox-ts'
import { useGolfCourses, useMapboxMap } from '@/composables'
import { setWeatherLocation, selectedIds } from '@/store';
import { log } from '@/utils'

const accessToken = import.meta.env.VITE_MAPBOX_TOKEN as string

const mapHandle = ref<Map | null>(null);

const onLoad = (map: Map) => {
  mapHandle.value = map
  log('map loaded?', map)
  useGolfCourses(map)
  setTimeout(()=> {
    const { addWeatherLayers } = useMapboxMap(map)
    addWeatherLayers(['radar'])
    
  }, 1000)
}

const handleResult = (result: any) => {
  if (mapHandle.value){
    const { clearHighlightedPoints } = useGolfCourses(mapHandle.value)
    setWeatherLocation(...result.center as [number, number])
    selectedIds.value = []
  }
  
}


</script>

<template>
  <div class="map-container">
    <mapbox-map 
      :accessToken="accessToken" 
      :center="[-93.263, 44.98]"
      :zoom="9"
      @loaded="onLoad"
    >
      <mapbox-geocoder-control @result="handleResult" /> 
      <mapbox-geolocate-control />
    </mapbox-map>
  </div>
</template>

<style lang="scss">
.map-container {
  height: calc(100vh - 60px);
  width: 100%;
}
</style>
