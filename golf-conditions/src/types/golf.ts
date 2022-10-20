import { components } from './api'

export type GolfCourse = components['schemas']['GolfCourse']
type FeatureCollection = components['schemas']['GeoJSONFeatureCollection']

export interface GolfCourseFeatureCollection extends FeatureCollection {
  features: GolfCourseFeature[];
}

type PointFeature = components['schemas']['PointFeature']

export type RatingResponse = components['schemas']['RatingResponse']
export type WeatherResponse = components['schemas']['WeatherConditionsResponse']

export interface GolfCourseFeature extends PointFeature {
  properties: GolfCourse;
}
