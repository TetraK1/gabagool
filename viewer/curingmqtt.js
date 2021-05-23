// Create a client instance
//client = new Paho.MQTT.Client("broker.hivemq.com", 8000, "clientId");
//client = new Paho.MQTT.Client("test.mosquitto.org", 8080, "clientId");
client = new Paho.MQTT.Client("broker.emqx.io", 8084, "clientId");

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

client.connect({onSuccess:onConnect});

function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("emberbox/#");
  //message = new Paho.MQTT.Message("Hello");
  //message.destinationName = "World";
  //client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
  client.connect({onSuccess:onConnect});
}

// called when a message arrives
function onMessageArrived(message) {
  console.log("onMessageArrived:"+message.payloadString);
  data = JSON.parse(message.payloadString);
  document.getElementById('temperature').innerHTML = data['data']['temperature'] + '&#176;';
  document.getElementById('humidity').innerHTML = data['data']['humidity'] + '%';
  document.getElementById('pressure').innerHTML = data['data']['pressure'] + ' Pa';
  document.getElementById('updatetime').innerHTML = new Date(data['time'] * 1000).toLocaleString();
}