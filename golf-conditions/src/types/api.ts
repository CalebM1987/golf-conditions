/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

export interface paths {
  "/golf-courses": {
    /** fetches all golf courses */
    get: operations["get_all_courses_golf_courses_get"];
  };
  "/golf-courses/{id}": {
    /** fetches a single golf course */
    get: operations["get_single_course_golf_courses__id__get"];
  };
  "/weather/{loc}": {
    /** fetch weather conditions at a given location */
    get: operations["get_weather_weather__loc__get"];
  };
  "/golf-conditions/{loc}": {
    /** fetch conditions for golfing at a given location */
    get: operations["golf_conditions_golf_conditions__loc__get"];
  };
}

export interface components {
  schemas: {
    /** GeoJSONFeatureCollection */
    GeoJSONFeatureCollection: {
      /** Type */
      type: string;
      /** Features */
      features: components["schemas"]["PointFeature"][];
    };
    /** GolfCourse */
    GolfCourse: {
      /** Id */
      id?: number;
      /** Region */
      Region?: number;
      /** Coursename */
      CourseName?: string;
      /** Address */
      Address?: string;
      /** City */
      City?: string;
      /** Zip */
      Zip?: string;
      /** State */
      State?: string;
      /** Holes */
      Holes?: number;
      /** Phone */
      Phone?: string;
      /** Latitude */
      Latitude?: number;
      /** Longitude */
      Longitude?: number;
    };
    /** HTTPValidationError */
    HTTPValidationError: {
      /** Detail */
      detail?: components["schemas"]["ValidationError"][];
    };
    /** IndexRange */
    IndexRange: {
      /** Min */
      min: number;
      /** Max */
      max: number;
      /** Reverse */
      reverse: boolean;
    };
    /** Indice */
    Indice: {
      /** Type */
      type: string;
      range: components["schemas"]["IndexRange"];
      past?: components["schemas"]["RatingIndex"];
      current: components["schemas"]["RatingIndex"];
    };
    /** LatLng */
    LatLng: {
      /** Lat */
      lat: number;
      /** Long */
      long: number;
    };
    /** Place */
    Place: {
      /** Name */
      name: string;
      /** State */
      state: string;
      /** Country */
      country: string;
    };
    /** PointFeature */
    PointFeature: {
      /** Type */
      type: string;
      geometry: components["schemas"]["PointGeometry"];
      /** Properties */
      properties?: unknown;
    };
    /** PointGeometry */
    PointGeometry: {
      /** Type */
      type: string;
      /** Coordinates */
      coordinates: number[];
    };
    /** Profile */
    Profile: {
      /** Tz */
      tz: string;
    };
    /** RatingIndex */
    RatingIndex: {
      /** Timestamp */
      timestamp: number;
      /** Datetimeiso */
      dateTimeISO: string;
      /** Index */
      index: number;
      /** Indexeng */
      indexENG: string;
    };
    /** RatingResponse */
    RatingResponse: {
      /** Success */
      success: boolean;
      /** Error */
      error?: string;
      /** Response */
      response: components["schemas"]["ResponseObject"][];
    };
    /** ResponseObject */
    ResponseObject: {
      loc: components["schemas"]["LatLng"];
      place: components["schemas"]["Place"];
      profile: components["schemas"]["Profile"];
      indice: components["schemas"]["Indice"];
    };
    /** ValidationError */
    ValidationError: {
      /** Location */
      loc: string[];
      /** Message */
      msg: string;
      /** Error Type */
      type: string;
    };
  };
}

export interface operations {
  /** fetches all golf courses */
  get_all_courses_golf_courses_get: {
    parameters: {
      query: {
        f?: string;
        id?: number;
        Region?: number;
        CourseName?: string;
        Address?: string;
        City?: string;
        Zip?: string;
        State?: string;
        Holes?: number;
        Phone?: string;
        Latitude?: number;
        Longitude?: number;
      };
    };
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": Partial<
            components["schemas"]["GeoJSONFeatureCollection"]
          > &
            Partial<components["schemas"]["GolfCourse"][]>;
        };
      };
      /** Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** fetches a single golf course */
  get_single_course_golf_courses__id__get: {
    parameters: {
      path: {
        id: number;
      };
    };
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["GolfCourse"];
        };
      };
      /** Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** fetch weather conditions at a given location */
  get_weather_weather__loc__get: {
    parameters: {
      path: {
        loc: string;
      };
    };
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
      /** Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** fetch conditions for golfing at a given location */
  golf_conditions_golf_conditions__loc__get: {
    parameters: {
      path: {
        loc: string;
      };
      query: {
        reverse?: boolean;
      };
    };
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["RatingResponse"];
        };
      };
      /** Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
}

export interface external {}
