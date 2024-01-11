/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      
      cloudant.setServiceUrl(params.COUCH_URL);
      try {
        let dbList = await cloudant.getAllDbs();
        return { "dbs": dbList.result };
      } catch (error) {
          return { error: error.description };
      }
}


cloudant_info = {
    IAM_API_KEY: "fill in your IAM API key",
    COUCH_URL:  "fill in your Cloudant URL"
}

main(cloudant_info).then((result) => {
    console.log(result);
}).catch((err) => {
    console.log(err);
});