doc = `
API Management Postman Test Runner

Usage:
  test-runner.js <service_name> <environment> [<base_path>]
  test-runner.js -h | --help

  -h --help  Show this text.
`

const docopt = require('docopt').docopt
const fs = require('fs')
const path = require('path')
const newman = require('newman')

function collectionRunner(serviceName, environmentName, basePath, credentials) {
  const collectionPath = path.resolve(`e2e/${serviceName}.collection.json`)
  const environmentPath = path.resolve(`e2e/environments/${environmentName}.postman.json`)

  const collection = JSON.parse(fs.readFileSync(collectionPath).toString())
  const environment = JSON.parse(fs.readFileSync(environmentPath).toString())
  const globals = overrideGlobals(basePath, credentials)

  const callback = err => {
    if (err) { throw err; }
    console.log('collection run complete!');
  }

  newman.run({
    collection,
    reporters: ['cli', 'junit'],
    reporter: {
      junit: {
        export: './test-report.xml'
      }
    },
    environment,
    globals

  }, callback)
    .on("start", () => {
      const filterValue = (e, key) => e['values'].filter(v => v.key === key)[0]['value']
      const url = `${filterValue(environment, "baseUrl")}${filterValue(globals, "basePath")}` //concatenates <baseUrl><basePath>

      console.log("accessToken", filterValue(globals, "accessToken"))
      console.log('Running against ' + url);
      console.log('Using collection file ' + collectionPath);
      console.log('Using environment file ' + environmentPath);
    })
}

function main(args) {
  const credentials = getCredentialsFromEnv()
  const serviceName = args['<service_name>']

  collectionRunner(serviceName, args['<environment>'], args['<base_path>'], credentials)
}

function getCredentialsFromEnv() {
  const accessToken = process.env['ACCESS_TOKEN']
  if (!accessToken) {
    throw new Error("ACCESS_TOKEN is required.")
  }

  const apiKey = process.env['API_KEY']
  if (!apiKey) {
    throw new Error("API_KEY is required.")
  }

  const statusApiKey = process.env['STATUS_APIKEY']
  if (!statusApiKey) {
    throw new Error("STATUS_APIKEY is required.")
  }

  return {
    accessToken: accessToken.trim(),
    apiKey: apiKey.trim(),
    statusApiKey: statusApiKey.trim(),
  }
}

function overrideGlobals(basePath, credentials) {
  const globals = JSON.parse(fs.readFileSync(path.resolve("e2e/globals.json")).toString())
  const values = globals["values"]

  const findAndOverride = (arr, key, value) => arr.filter(v => v.key === key).map(v => ({...v, value}))[0]

  const newValues = [
    findAndOverride(values, "basePath", basePath),
    findAndOverride(values, "accessToken", credentials.accessToken),
    findAndOverride(values, "apiKey", credentials.apiKey),
    findAndOverride(values, "statusApiKey", credentials.statusApiKey),
  ]

  globals['values'] = newValues

  return globals
}

args = docopt(doc)
main(args)
