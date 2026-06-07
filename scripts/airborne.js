
// <![CDATA[
var speed=20; // speed of flight, lower is faster
var count=250; // number of frames before animation complete

/***************************\
*    Airborne Text Effect   *
*(c) 2003-6 mf2fm web-design*
*  http://www.mf2fm.com/rv  *
* DON'T EDIT BELOW THIS BOX *
\***************************/
var airbon, airtxt, airtop, airlef;
var swide=800;
var shigh=600;
var frame=count;
var ax=new Array();
var ay=new Array();
window.addEventListener('load', function() { if (document.getElementById) {
  var i, y, airme, airli;
  set_width();
  airbon=document.getElementById("airborne");
  if (!document.all) airbon.style.position="relative"; // ie bug fix
  airtxt=airbon.firstChild.nodeValue;
  while (airbon.childNodes.length) airbon.removeChild(airbon.childNodes[0]);
  for (i=0; i<airtxt.length; i++) {
    airli=document.createElement("span");
    airli.setAttribute("id", "airb"+i);
    airli.appendChild(document.createTextNode(airtxt.charAt(i)));
    airbon.appendChild(airli);
  }
  y=getPageTop(airbon);
  for (i=0; i<airtxt.length; i++) ax[i]=getPageLeft(document.getElementById("airb"+i));
  for (i=0; i<airtxt.length; i++) {
    if (Math.random()<0.5) {
      ax[i]=((Math.random()<0.5)?0:swide)-ax[i];
      ay[i]=(Math.floor(Math.random()*shigh))-y;
    }
    else {
      ay[i]=((Math.random()<0.5)?0:shigh)-y;
      ax[i]=(Math.floor(Math.random()*swide))-ax[i];
    }
    airme=document.getElementById("airb"+i);
    airme.style.position="relative";
    airme.style.left=ax[i]+"px";
    airme.style.top=ay[i]+"px";
  }
  fly_me();
}});

function set_width() {
  if (typeof(self.innerWidth)=="number") {
    swide=self.innerWidth;
    shigh=self.innerHeight;
  }
  else if (document.documentElement && document.documentElement.clientWidth) {
    swide=document.documentElement.clientWidth;
    shigh=document.documentElement.clientHeight;
  }
  else if (document.body.clientWidth) {
    swide=document.body.clientWidth;
    shigh=document.body.clientHeight;
  }
}

function getPageLeft(el) {
  var x=0;
  do { x+=el.offsetLeft }
  while ((el=el.offsetParent)!=null) ;
  return x;
}

function getPageTop(el) {
  var y=0;
  do { y+=el.offsetTop }
  while ((el=el.offsetParent)!=null) ;
  return y;
}

function fly_me() {
  var airme;
  for (var i=0; i<airtxt.length; i++) {
	ax[i]-=swide*ax[i]*Math.random()/(frame*(count-1));
	ay[i]-=shigh*ay[i]*Math.random()/(frame*(count-1));
    airme=document.getElementById("airb"+i);
	airme.style.left=Math.round(ax[i])+"px";
	airme.style.top=Math.round(ay[i])+"px";
  }
  if (--frame) setTimeout("fly_me()", speed);
}
// ]]>
