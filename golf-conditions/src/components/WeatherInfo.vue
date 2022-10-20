<script lang="ts" setup>
import { computed, reactive,ref,  watch } from 'vue'
import { getGolfConditions } from '@/services'
import { GolfCourse } from '@/types';

interface Props {
  course: GolfCourse;
}

const props = defineProps<Props>()
// const conditions = ref<any>({})

watch(()=> [props.course], async (course)=> {
  console.log('course changed')
  
  const { data } = await getGolfConditions({ loc: `${props.course.Latitude},${props.course.Longitude}`})
  conditions.value = data
})

const { data } = await getGolfConditions({ loc: `${props.course.Latitude},${props.course.Longitude}`})
console.log('data?', data)
const conditions = ref(data as any)
console.log('conditions: ', conditions.value)
const weather = reactive(conditions.value?.periods[0]?.weather)
const temp = computed(()=> conditions.value?.periods[0]?.temp)
const icon = computed(()=> weather.value?.phrase)

</script>

<template>
  <q-card class="golf-conditions">
    <q-card-section>
      <div class="text-h6">Weather Conditions</div>
      <div class="text-subtitle2">{{ conditions.place.name}}, {{ conditions.place.state}}</div>
    </q-card-section>
    <q-separator />
    <q-card-section>
      <div class="text-subtitle2">

        <q-icon name="thermometer" color="negative" size="1.25rem" />
        <p><span style="font-size: 1.3rem;">{{ parseInt(temp.avgF) }}</span>°F</p>
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
    <q-card-section>
    </q-card-section>
  </q-card>
</template>