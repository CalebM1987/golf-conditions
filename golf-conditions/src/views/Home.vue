<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';

const MapView = defineAsyncComponent(()=> import('./MapView.vue'))
</script>

<template>

  <Suspense>
    <map-view />
    <template #fallback>
      <div class="q-pa-xl map-loader mobile">
        <q-spinner-facebook
          class="mx-auto my-auto"
          color="primary"
          size="2em"
        >
          <p>loading map...</p>
        </q-spinner-facebook> 
      </div>
    </template>
  </Suspense>
  
</template>