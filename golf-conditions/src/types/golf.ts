import { components } from './api'

export type GolfCourse = components['schemas']['GolfCourse']
type FeatureCollection = components['schemas']['GeoJSONFeatureCollection']

export interface GolfCourseFeatureCollection extends FeatureCollection {
  features: GolfCourseFeature[];
}

type PointFeature = components['schemas']['PointFeature']

export interface GolfCourseFeature extends PointFeature {
  properties: GolfCourse;
}
