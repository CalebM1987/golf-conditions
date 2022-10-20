import path from 'path'
import fs from 'fs'
import fetch from 'node-fetch'
import Cheerio from 'cheerio'

/** region names */
const regions = [
  'brainerd-lakes-area-mn',
  'metro-mn',
  'southern-mn',
  'west-central-mn',
  'northwest-mn',
  'northeast-mn'
]


/**
 * helper function to crawl data from (must visit a region) for mn golf courses
 * https://minnesotagolf.com/fairways 
 */
const getCourseInfo = async (region) => {

  const url = `https://minnesotagolf.com/fairways/${region}/` 

  const response = await fetch(url)
  const text = await response.text()

  // const root = parse(text)
  const $ = Cheerio.load(text)
  
  const table = $('table')
  // get body 
  const body = table.find('tbody')
  // create array of rows
  const features = []

  // get headers
  const headers = []
  $(body.find('tr:first')).children('td').each((i, c) => {
    headers.push($(c).text().replace(' ', '').replace('#', ''))
  })
  console.log('headers: ', headers)

  // iterate all other table rows to build csv
  $(body.find('tr')).each((ri, tr)=> {
    if (ri > 0){
      const vals = []
      $(tr).children('td').each((i, c) => {
        vals.push($(c).text())
      })
      
      // check for course name
      if (vals[0]){
        features.push(
          headers.reduce((o, h, i)=> ({...o, [h]: vals[i]}), {})
        )
      }
    }
    
  })

  // write json file
  const jsonFile = path.resolve(`./app/data/${region}.json`)
  fs.writeFile(jsonFile, JSON.stringify(features, null, 2), (err)=> {
    if (err){
      console.warn('failed to save json file', err)
    } else {
      console.log(`successfully saved "${region}.json" file`)
    }
  })

  return features

}

/**
 * joins marker data to tabular data
 * @param {*} region 
 * @param {*} features 
 * @returns 
 */
async function joinData(region, features){
  const jsonFile = path.resolve(`./app/data/${region.replace('-mn', '')}.json`)
  const rawData = fs.readFileSync(jsonFile)
  const { markers } = JSON.parse(rawData)
  
  features.forEach(ft => {
    const course = markers.find(m => m.title.toLowerCase() === ft.CourseName.toLowerCase())
    if (course){
      ft.Latitude = parseFloat(course.lat)
      ft.Longitude = parseFloat(course.lng)
      ft.id = parseInt(course.id)
      ft.Region = parseInt(course.map_id)
      ft.State = 'MN'
    }
    ft.Holes = parseInt(ft.Holes)
  })

  return features
}

/**
 * download tabular data and join to markers data
 */
async function crawlRegions(){
  const allCourses = []
  for await (const region of regions) {
    const data = await getCourseInfo(region)
    const features = await joinData(region, data)
    allCourses.push(...features.filter(f => f.Latitude && f.Longitude))
  }

  // write json file
  const allFeatsFile = path.resolve(`./app/data/All_MN_Courses.json`)
  fs.writeFile(allFeatsFile, JSON.stringify(allCourses, null, 2), (err)=> {
    if (err){
      console.warn('failed to save json file', err)
    } else {
      console.log(`successfully saved all courses file`)
    }
  })

}

// run it
crawlRegions()

