const data = require('./data.js');
const contentful = require('contentful-management');

const client = contentful.createClient({
  accessToken: 'CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6'
});

client.getSpace('wjuty07n9kzp')
  .then((space) => space.getEnvironment('Master'))
  .then((environment) => {
    data.forEach((item) => {
      environment.createEntry('testShane', item)
        .then((entry) => {
          console.log(entry);
          entry.publish();
        })
        .catch(console.error);
    });
  });
