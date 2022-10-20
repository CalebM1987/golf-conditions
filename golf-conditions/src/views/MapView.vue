<script lang="ts" setup>
import { MapboxMap } from 'vue-mapbox-ts'
import { Map } from 'mapbox-gl'
import { useGolfCourses, useMapboxMap } from '@/composables'
import { setWeatherLocation } from '@/store';

const accessToken = import.meta.env.VITE_MAPBOX_TOKEN as string

const onLoad = (map: Map) => {
  console.log('map loaded?', map)
  useGolfCourses(map)
  setTimeout(()=> {
    const { addWeatherLayers } = useMapboxMap(map)
    addWeatherLayers(['radar'])
  }, 1000)
}

const handleResult = (result: any) => {
  setWeatherLocation(...result.center as [number, number])
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
