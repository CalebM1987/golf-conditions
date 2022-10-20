<script lang="ts" setup>
import { defineAsyncComponent, computed, ref, onMounted } from 'vue';
import { golfCourses, selectedIds } from '@/store'

const GolfCourseInfo = defineAsyncComponent(()=> import('@/components/GolfCourseInfo.vue'))
const WeatherInfo = defineAsyncComponent(()=> import('@/components/WeatherInfo.vue'))

const selectedFeatures = computed(()=> golfCourses.value.filter(gc => selectedIds.value.includes(gc.properties.id!)))
const selectedIndex = ref(0)

const selectedFeature = computed(()=> selectedFeatures.value[selectedIndex.value])

const next = ()=> {
  if (selectedIndex.value >= selectedFeatures.value.length){
    selectedIndex.value++
  } else {
    selectedIndex.value = 0
  }
}

const prev = ()=> {
  if (selectedIndex.value >= 1){
    selectedIndex.value--
  } else if (selectedFeatures.value.length){
    selectedIndex.value = selectedFeatures.value.length - 1
  } else {
    selectedIndex.value = 0
  }
}

onMounted(()=> console.log('mounted sidebar'))

//@ts-ignore
window.selected = selectedFeature.value
</script>

<template>
  <div class="context-area">
    <golf-course-info :course="selectedFeature?.properties" class="q-ma-sm" />

    <Suspense>
      <weather-info :course="selectedFeature.properties" v-if="selectedFeature" class="q-ma-sm" />
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