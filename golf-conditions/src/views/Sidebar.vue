<script lang="ts" setup>
import { defineAsyncComponent, computed, ref, onMounted } from 'vue';
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

onMounted(()=> console.log('mounted sidebar'))

const hasLocation = computed(()=> weatherLocation.value.lat)

//@ts-ignore
window.selected = selectedFeature
//@ts-ignore
window.loc = weatherLocation
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