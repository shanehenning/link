module.exports = contentfulMethods

// const data = require('./test-output.js');
const contentful = require('contentful-management');
var contentfulMethods = {}

const client = contentful.createClient({
  accessToken: 'CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6'
});


contentfulMethods.createEntry = function() {
  client.getSpace('wjuty07n9kzp')
    .then((space) => space.getEnvironment('Feature'))
    .then((environment) => {
      data.forEach((item) => {
        environment.createEntry('testShane', item)
          .then((entry) => {
            console.log(entry);
            // entry.publish();
          })
          .catch(console.error);
      });
    });
}

contentfulMethods.getEntry = function(){
  client.getSpace('wjuty07n9kzp')
  .then((space) => space.getEnvironment('Feature'))
  .then((environment) => environment.getEntry('80e0e9de3a58809305de74'))
    .then((response) => {
      response = squashResponse(response)
      console.log('response: ', response);
    })
    .catch(console.error)
}

contentfulMethods.getContentByType = function(type){
  client.getSpace('wjuty07n9kzp')
  .then((space)=> space.getEnvironment('Feature'))
  .then((environment) => environment.getEntries({
    content_type: type,
    select: 'fields'
  }))
  .then((response) => {
    var activities = []
    response.items.forEach((item, idx) =>{
      activities.idx = item['fields']
    })
    console.log('activities: ', activities);
  })
  .catch(console.error)
}
contentfulMethods.getContentByType('advisoryActivityServiceLearning');

contentfulMethods.getAdvisories = function(){
  client.getSpace('wjuty07n9kzp')
  .then((space)=> space.getEnvironment('Feature'))
  .then((environment) => environment.getEntries())
  .then((response) => {
    console.log('response: ', response);
  })
  .catch(console.error)
}

const squashResponse = obj => {
  const fields = obj['fields']
  for (const prop in fields) {
    fields[prop] = fields[prop]['en-US']
  }
  obj['fields'] = fields
  return obj
}
