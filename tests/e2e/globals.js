doc = `
API Management Postman Test Runner
Usage:
  test-runner.js <username> <password> <apigee_environment> <base_url> <apikey> <token_app_url>
  test-runner.js -h | --help
  -h --help  Show this text.
`

const fs = require('fs')
const docopt = require('docopt').docopt
const puppeteer = require('puppeteer')

function nhsIdLogin(username, password, apigee_environment, base_url, apikey, login_url, writeGlobals, writeEnvVariables) {
  (async () => {
    console.log('Oauth journey on ' + login_url)

    const browser = await puppeteer.launch({
      executablePath: process.env.CHROME_BIN || null,
      args: ['--no-sandbox', '--headless', '--disable-gpu']
    });

    const page = await browser.newPage()
    await page.goto(login_url, { waitUntil: 'networkidle2' })
    await page.click('#start')
    await page.waitForSelector('#idToken1', { timeout: 130000 })
    await page.type('#idToken1', username)
    await page.type('#idToken2', password)
    await page.click('#loginButton_0')
    await page.waitForNavigation()

    let credentialsJSON = await page.$eval('body > div > div > pre', e => e.innerText)
    let credentials = credentialsJSON.replace(/'/g, '"')
    let credentialsObject = JSON.parse(credentials)

    await browser.close();

    writeGlobals(credentialsObject.access_token, apikey)
    writeEnvVariables(base_url, apigee_environment)
  })()
}

function writeGlobals(token, apikey) {
  fs.copyFileSync("e2e/local.globals.json", "e2e/deploy.globals.json");

  let globals = JSON.parse(fs.readFileSync("e2e/deploy.globals.json"));

  const tokenGlobal = {
    "key": "token",
    "value": token,
    "enabled": true
  };

  const apikeyGlobal = {
    "key": "apikey",
    "value": apikey,
    "enabled": true
  };

  for(let i = 0; i < globals.values.length; i++) {
    if (globals.values[i].key === "token") {
      globals.values[i] = tokenGlobal;
    }
    if (globals.values[i].key === "apikey") {
      globals.values[i] = apikeyGlobal;
    }
  }

  fs.writeFileSync('e2e/deploy.globals.json', JSON.stringify(globals));
}

function writeEnvVariables(base_url, apigee_environment){
  let envVariables = JSON.parse(fs.readFileSync(`e2e/environments/${apigee_environment}.postman.json`));
  const baseUrl = {
    "key": "base_url",
    "value": base_url,
    "enabled": true
  };
  if (envVariables.values[0].key === "base_url") {
    envVariables.values[0] = baseUrl;
  }
  fs.writeFileSync(`e2e/environments/deploy.${apigee_environment}.postman.json`, JSON.stringify(envVariables));
}

function main(args) {
  nhsIdLogin(
    args['<username>'],
    args['<password>'],
    args['<apigee_environment>'],
    args['<base_url>'],
    args['<apikey>'],
    args['<token_app_url>'],
    writeGlobals,
    writeEnvVariables,
  )
}

args = docopt(doc)
main(args)
