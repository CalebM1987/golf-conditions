<script lang="ts" setup>
import { computed, reactive,ref,  watch } from 'vue'
import { getGolfConditions, getCurrentWeatherConditions } from '@/services'
import { weatherLocation } from '@/store'
import { ILngLat, RatingResponse, WeatherResponse } from '@/types'

const isLoading = ref(true)

const conditions = ref<RatingResponse | undefined>()
const weather = ref<WeatherResponse | undefined>()

interface Props {
  latLng: ILngLat;
}

const props = defineProps<Props>()

watch(()=> [props.latLng], async ([loc])=> {
  if (loc?.lat){
    try {
      isLoading.value = true
      const location = `${loc.lat},${loc.lng}`
      const { data } = await getGolfConditions({ loc: location})
      const { data: weatherData } = await getCurrentWeatherConditions({ loc: location })
      conditions.value = data
      weather.value = weatherData
    } catch(err){
      console.warn('failed to fetch golf conditions: ', err)
    } finally {
      isLoading.value = false
    }
  }
})


if (props.latLng.lat){
    
  try {
      isLoading.value = true
      const location = `${weatherLocation.value!.lat},${weatherLocation.value!.lng}`
      const { data } = await getGolfConditions({ loc: location})
      const { data: weatherData } = await getCurrentWeatherConditions({ loc: location })
      conditions.value = data
      weather.value = weatherData
    } catch(err){
      console.warn('failed to fetch golf conditions: ', err)
    } finally {
      isLoading.value = false
    }
}

const rating = computed(()=> conditions.value?.response[0]?.indice?.current)
const weatherConditions = computed(()=> weather.value?.periods[0])
const temp = computed(()=> weatherConditions.value?.temp ?? undefined)

</script>

<template>
  <q-card class="golf-conditions">
   
    <q-card-section>
      <div class="text-h6">Weather Conditions</div>
      <div class="text-subtitle2 text-italic text-gray" v-if="weather && !isLoading">{{ weather?.place?.name}}, {{ weather?.place?.state}}</div>
    </q-card-section>
    <q-separator />

    <q-card-section v-if="conditions && !isLoading">
      <q-card-section>
        <div class="text-subtitle2">
          <p><span style="font-size: 1.3rem;">{{ Math.round(temp?.avgF ?? 0) }}</span>°F</p>
          <p>{{ weatherConditions?.weather?.phrase ?? 'N/A' }}</p>
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section v-if="rating?.index">
        <p>Golf Conditions for Today ({{ rating!.index }}/5)</p>
        <q-rating
          readonly
          v-model="rating!.index"
          size="2em"
          :max="5"
          class="cursor-pointer"
          color="warning"
        />
          
        <q-tooltip class="bg-primary">conditions are {{ rating.indexENG }}</q-tooltip>
        
      </q-card-section>
   </q-card-section>

    <q-card-section v-if="isLoading">
      
      <q-spinner-oval
        class="mx-auto my-auto"
        color="primary"
        size="2em"
      >
        <p>loading weather conditions</p>
      </q-spinner-oval>
    </q-card-section>
  </q-card>
</template>