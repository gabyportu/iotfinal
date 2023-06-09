window.addEventListener('load', getReadings);
var stateButton = 0;
var flag  = 0;
function sendAction1(val){
  
  if(stateButton == 0){
      stateButton = 1;
  }else{
      stateButton = 0;
  }
  changeStateLight();
  var xhttp = new XMLHttpRequest();
  xhttp.open("PUT", "/TURN?PAGE="+val+"&VALUE="+stateButton, true);
  xhttp.send(); 
}

function changeStateLight(){
  console.log(stateButton);
  var pulsadorButton = document.getElementById("pulsador-button");
  var pulsadorButton2 = document.getElementById("img2");
  
  
  if(stateButton == 0){
      pulsadorButton.src = "media/cum1.png";
      pulsadorButton2.src = "media/horno4.png";
      document.getElementById("pulsador-button").classList.remove("pulsador-activado");
      document.getElementById("img2").classList.remove("pulsador-activado2");
      document.body.style.backgroundColor = "white";
  }else{
      pulsadorButton.src = "media/cum2.png";
      pulsadorButton2.src = "media/horno3.png";
      document.getElementById("pulsador-button").classList.add("pulsador-activado");
      document.getElementById("img2").classList.add("pulsador-activado2");
      document.body.style.backgroundColor = "#E3DFFD";
  }
  
}

function sendAction2(val){
  
  if(stateButton == 0){
      stateButton = 1;
  }else{
      stateButton = 0;
  }
  changeStateLight();
  var xhttp = new XMLHttpRequest();
  //cambiar el valor por la del sensor
  xhttp.open("PUT", "/TURN?PAGE="+val+"&VALUE="+stateButton, true);
  xhttp.send(); 
}

function getReadings(){
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var myObj = JSON.parse(this.responseText);
      console.log(myObj);
      receiveJson(myObj);
      
      signalChanger(parseInt(myObj.rssi)*-1);
      
     
    }
  }; 
  xhr.open("GET", "/readings", true);
  xhr.send();
}

function updateValuesInFront(
  rssi,
  ip,
  hostname,
  wifiStatus,
  ssid, 
  psk,
  bssid,
  statusFoco,
  pwm,
  limldr
){
  if(pageCurrent == 4){
    document.getElementById("ldrlimval").innerHTML = limldr;
  }
  
   
  if(pageCurrent === 2){
    document.getElementById("pwmslider").value = pwm;
    document.getElementById("pwm_value3").innerHTML = pwm
  }
  
  stateButton = statusFoco;
  changeStateLight();
  buildTable(ip,hostname, wifiStatus, ssid,psk,bssid, rssi);
}
function buildTable(ip, hostname, wifi_status, ssid, psk , bssid, rssi){
  document.getElementById("ip").innerHTML = ip;
  document.getElementById("hn").innerHTML = hostname;
  document.getElementById("st").innerHTML = wifi_status;
  document.getElementById("ss").innerHTML = ssid;
  document.getElementById("ps").innerHTML = psk;
  document.getElementById("bs").innerHTML = bssid; 
  document.getElementById("rs").innerHTML = rssi; 
    
}

function buildTable(ip, hostname, wifi_status, ssid, psk , bssid){
  document.getElementById("ip").innerHTML = ip;
  document.getElementById("hn").innerHTML = hostname;
  document.getElementById("st").innerHTML = wifi_status;
  document.getElementById("ss").innerHTML = ssid;
  document.getElementById("ps").innerHTML = psk;
  document.getElementById("bs").innerHTML = bssid; 
    
}