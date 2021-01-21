var redis = require('redis'),
rd = redis.createClient();

rd.on('error', function(err){
    console.log('Error ' + err);
});


console.log('Connection is establishing now...');
rd.get("user:123", redis.print);
for(i=0; i < 10; i++){
    rd.set("test:"+i, "Hello")
}
