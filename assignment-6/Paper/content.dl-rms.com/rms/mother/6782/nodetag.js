(function(){
var pfs={ "http://online.wsj.com/home-page":{"nid":32400,"tr":1,"ex":"http://online.wsj.com/public/us$|http://[a-zA-Z.]*allthingsd.com|http://online.wsj.com/home-page$|http://www.marketwatch.com/$|http://www.smartmoney.com/$|http://www.fins.com/$|http://online.barrons.com/home-page$"} },d=document,w=window,u=(w.gm_fake_href)?w.gm_fake_href:w.location.href;

function z(n){
var s,u;

if (Math.random()>=n['tr']) {
	return;
}



s=d.createElement('SCRIPT');
u='//content.dl-rms.com/dt/s/'+n['nid']+'/s.js';
s.src=u;
s.type='text/javascript';
d.getElementsByTagName('head')[0].appendChild(s);
}
function r() {
	var n="",p,x;
	while (1) {
		try {
			for (p in pfs) {
			  if (u.substring(0,p.length)==p && p.length > n.length) {
				if (pfs[p].ex) {
					x=new RegExp(pfs[p].ex,"i");
					if (x.test(u)) {
						continue;
					}
				}
				n=p;
			  }
			}
			if (n.length > 0) {
				z(pfs[n]);
				return;
			}
		} catch (e) {}
	
		if (w==top) {
			break;
		}
	
		if (w==window&&u!=d.referrer) {
			u=d.referrer;
		} else {
			w=w.parent;
		}
	}
}

if (d.readyState=="complete"){
	r();
} else if (w.addEventListener){ 
	w.addEventListener("load", r, false);
} else if (w.attachEvent){ 
	w.attachEvent("onload", r);
}
})();
