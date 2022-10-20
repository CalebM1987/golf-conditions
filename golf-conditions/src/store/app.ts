import { GolfCourseFeature } from './../types/golf';
import { ref, reactive } from 'vue'


export const baseUrl = ref('http://127.0.0.1:8000')

export const golfCourses = ref<GolfCourseFeature[]>([])

export const selectedIds = ref<number[]>([])