<script lang="ts" setup>
import { computed, reactive,ref,  watch } from 'vue'
import { getGolfConditions } from '@/services'
import { weatherLocation } from '@/store'
import { ILngLat, RatingResponse } from '@/types'

const isLoading = ref(true)

const conditions = ref<RatingResponse | undefined>()

interface Props {
  latLng: ILngLat;
}

const props = defineProps<Props>()

watch(()=> [props.latLng], async ([loc])=> {
  if (loc?.lat){
    try {
      isLoading.value = true
      const { data } = await getGolfConditions({ loc: `${loc.lat},${loc.lng}`})
      conditions.value = data
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
      const { data } = await getGolfConditions({ loc: `${weatherLocation.value!.lat},${weatherLocation.value!.lng}`})
      conditions.value = data
    } catch(err){
      console.warn('failed to fetch golf conditions: ', err)
    } finally {
      isLoading.value = false
    }
}

const weather = computed(()=> conditions.value?.periods[0]?.weather ?? undefined)
const temp = computed(()=> conditions.value?.periods[0]?.temp ?? undefined)

</script>

<template>
  <q-card class="golf-conditions">
   
    <q-card-section>
      <div class="text-h6">Weather Conditions</div>
      <div class="text-subtitle2 text-italic text-gray" v-if="conditions && !isLoading">{{ conditions?.place?.name}}, {{ conditions?.place?.state}}</div>
    </q-card-section>
    <q-separator />

    <q-card-section v-if="conditions && !isLoading">
      <q-card-section>
        <div class="text-subtitle2">
          <p><span style="font-size: 1.3rem;">{{ Math.round(temp?.avgF ?? 0) }}</span>°F</p>
          <p>{{ weather?.phrase ?? 'N/A' }}</p>
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section>
        <p>Golf Conditions for Today ({{ conditions.rating }}/5)</p>
        <q-rating
          v-model="conditions.rating"
          size="2em"
          :max="5"
          color="warning"
        />
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