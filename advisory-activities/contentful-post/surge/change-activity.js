function composeRequest(space_id, environment_id, access_token, content_type){
  var url = `/spaces/${space_id}/environments/${environment_id}/entries?access_token=${access_token}&content_type=${content_type}`
}

$.get(url, function(data){
  console.log('data: ', data);
});
