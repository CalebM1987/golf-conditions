import { Fetcher, OpReturnType } from "openapi-typescript-fetch";
import { paths } from '@/types'

const api = Fetcher.for<paths>()

export const getGolfCourses = api.path('/golf-courses').method('get').create()
export const getCurrentWeatherConditions = api.path('/weather/{loc}').method('get').create()
export const getGolfConditions = api.path('/golf-conditions/{loc}').method('get').create()