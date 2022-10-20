<script lang="ts" setup>
import { computed } from 'vue'
import { GolfCourse } from '@/types'

interface Props { 
  course: GolfCourse;
}

const props = defineProps<Props>()

const directions = computed(()=> `http://maps.google.com/maps?q=${props.course.Address}%2C+${props.course.State}+${props.course.Zip}`)
</script>

<template>
  <q-card>
    <q-card-section v-if="course">
      <q-card-section>
        <div class="text-h6">{{ course.CourseName }}</div>
        <div class="text-subtitle2">
          <q-icon name="golf_course" color="negative" size="1.25rem" />
        {{ course.Holes }} holes
        </div>
      </q-card-section>
      <q-separator />

      <q-card-section>
        <p>{{ course.City }}, {{ course.State }}</p>
        <p>
          <q-icon name="location_on" color="primary" class="q-mr-sm" />
          <a :href="directions" target="_blank">{{ course.Address }}, {{ course.State }} {{ course.Zip }}</a>
        </p>

        <p>
          <q-icon name="call" color="primary" class="q-mr-sm" />
          <a :href="`tel:${course.Phone}`" v-if="course.Phone">{{ course.Phone }}</a>
        </p>
      </q-card-section>
    </q-card-section>

    <q-card-section v-else>
      <div class="text-h6 q-pa-xl">No Course Selected</div>
    </q-card-section>
  </q-card>

</template>