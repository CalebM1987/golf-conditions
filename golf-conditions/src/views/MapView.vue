<script lang="ts" setup>
import { MapboxMap } from 'vue-mapbox-ts'
import { Map } from 'mapbox-gl'
import { useGolfCourses } from '@/composables'

const accessToken = import.meta.env.VITE_MAPBOX_TOKEN as string

const onLoad = (map: Map) => {
  console.log('map loaded?', map)
  useGolfCourses(map)

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
      <mapbox-geocoder-control /> 
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
