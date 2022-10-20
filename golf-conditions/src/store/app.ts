import { GolfCourseFeature, ILngLat } from '@/types';
import { ref, computed } from 'vue'

export const baseUrl = ref(import.meta.env.PROD ? '/': 'http://127.0.0.1:8000')

export const golfCourses = ref<GolfCourseFeature[]>([])

export const selectedIds = ref<number[]>([])

export const selectedFeatures = computed(()=> golfCourses.value.filter(gc => selectedIds.value.includes(gc.properties.id!)))

export const selectedIndex = ref(0)

export const selectedFeature = computed(()=> selectedFeatures.value[selectedIndex.value])

export const weatherLocation = ref<ILngLat>({ lng: undefined, lat: undefined})

export const setWeatherLocation = (lng: number, lat: number) => weatherLocation.value = { lng: parseFloat(lng?.toFixed(4)) ?? undefined, lat: parseFloat(lat?.toFixed(4)) ?? undefined }

export const nextFeature = ()=> {
  if (selectedIndex.value >= selectedFeatures.value.length){
    selectedIndex.value++
  } else {
    selectedIndex.value = 0
  }
}

export const prevFeature = ()=> {
  if (selectedIndex.value >= 1){
    selectedIndex.value--
  } else if (selectedFeatures.value.length){
    selectedIndex.value = selectedFeatures.value.length - 1
  } else {
    selectedIndex.value = 0
  }
}