<script lang="ts" setup>
import { defineAsyncComponent, computed, } from 'vue';
import { 
  golfCourses, 
  selectedIds, 
  selectedFeature, 
  nextFeature, 
  prevFeature,
  weatherLocation 
} from '@/store'

const GolfCourseInfo = defineAsyncComponent(()=> import('@/components/GolfCourseInfo.vue'))
const WeatherInfo = defineAsyncComponent(()=> import('@/components/WeatherInfo.vue'))

const hasLocation = computed(()=> weatherLocation.value.lat)
</script>

<template>
  <div class="context-area">
    <golf-course-info :course="selectedFeature?.properties" class="q-ma-sm" />

    <Suspense>
      <weather-info class="q-ma-sm" :lat-lng="weatherLocation" v-if="hasLocation" />
      <template #fallback>
        <div class="q-pa-xl map-loader mobile">
          <q-spinner-facebook
            class="mx-auto my-auto"
            color="primary"
            size="2em"
          >
            <p>loading weather conditions...</p>
          </q-spinner-facebook> 
        </div>
      </template>
    </Suspense>
  </div>

</template>