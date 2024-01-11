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
    IAM_API_KEY: "rPnaY-vOBNNyYso8OV8I-blbzPLVEVC4cav9HJu_KanU",
    COUCH_URL:  "https://2fb1c265-3843-44c8-ab91-5a01d1e387b8-bluemix.cloudantnosqldb.appdomain.cloud"
}

main(cloudant_info).then((result) => {
    console.log(result);
}).catch((err) => {
    console.log(err);
});