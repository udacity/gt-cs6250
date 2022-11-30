S9Multipack=true;
S9MultipackRegistry={};
amznJQ.onReady("jQuery",function(){(function(b){var e=b(window);
var d=false;
e.load(function(){d=true
});
b.fn.s9Multipack=function(g){var f={minItems:3,maxItems:7,minItemWidth:155,seeded:false,seedHeaderBottomPadding:0,deferImageFlip:false,containerHorizontalPadding:0,suppressInitialResize:false,suppressImageFlip:false};
g=b.extend({},f,g);
this.each(function(){new a(b(this),g)
});
return this
};
function c(i){var g;
function f(){if(!g){h();
g=setTimeout(function(){h();
g=null
},500)
}}function h(){var j=true;
b.each(S9MultipackRegistry[i],function(){this.updateSizes(j);
j=false
})
}return{handleResizeEvent:f}
}function a(i,j){this.options=j;
this.updateSizes=x;
this.getColumnCount=h;
if(!window.S9MultipackResizer){throw"window.S9MultipackResizer not found on "+i[0].id
}var v=b(".s9SeedItem",i);
var t=b(".s9OtherItems",i);
var r=b(".asin",t);
var s=i.parents(".unified_widget, .widget");
s.addClass("s9Multipack");
var g=s.parent()[0].id;
var A,o,p,f,m;
var y;
if(j.seeded){A=b(".asin",v);
o=b(".s9_header.seed_header, .s9_header_o.seed_header_o",v);
f=o.children();
p=b(".s9_header.other_header, .s9_header_o.other_header_o",t);
m=p.children();
y=p.height();
var l=parseInt(p.css("margin-bottom"),10);
if(l>0){y+=l
}}else{y=0
}var z=j.minItems;
var u=z;
if(!j.suppressInitialResize){x(true,true)
}w(this);
if(jQuery.browser.msie){n()
}i.data("s9Multipack",this);
function w(C){if(g){var B=S9MultipackRegistry[g];
if(!B){B=S9MultipackRegistry[g]=[];
S9MultipackRegistry[g].master=C;
e.resize(new c(g).handleResizeEvent)
}B.push(C)
}else{e.resize(function(){x(true)
})
}i.bind("s9MultipackResize",function(E,D){x(true,D)
})
}function x(D,B){var E,C;
E=S9MultipackResizer(i[0],j.minItems,j.maxItems,j.minItemWidth,j.seeded,j.containerHorizontalPadding,!D);
C=E.potentialCols;
if(B||C!=u){u=C;
z=E.cols;
setTimeout(function(){k();
if(j.seeded){q()
}});
i.trigger("s9MultipackColumnCountChanged",E)
}}function q(){var B=Math.max(f[0].offsetHeight,m[0].offsetHeight);
o.css("height",B+"px");
p.css("height",B+"px");
i.css("padding-bottom",B+(j.seedHeaderBottomPadding?j.seedHeaderBottomPadding:0)+"px")
}function k(){if(j.suppressImageFlip){return
}if(j.deferImageFlip&&!d){e.load(k);
return
}var B=function(C){C.find("img").each(function(){if(this.getAttribute("url")){var D=b(this);
D.attr({src:D.attr("url"),url:""})
}})
};
B(r.slice(0,z));
if(j.seeded){B(A)
}}function n(){if(!d){e.load(function(){setTimeout(function(){x(true)
})
})
}}function h(){return z
}}b(function(){if(!b(".s9AddToCartHoverMain").length){return
}if("ontouchstart" in window){return
}b('<div id="s9AddToCartHoverContainer" style="position: relative; left: 0px; top: 0px; z-index: 1200"><div style="position: absolute; left: 0px; top: 0px"></div></div>').prependTo(b("body"));
var g=b("#s9AddToCartHoverContainer").children();
var f=null;
b(".s9hl").each(function(){var m=150;
var p=200;
var i=null;
var u=null;
var j=b(".s9AddToCartHoverMain",this);
var k=null;
var v=b(j.parents(".asin").get(0));
var r=v;
var y=b(j.children(".s9AddToCartHoverRight").get(0));
var t=8;
if(!(j&&j.length&&j.length>0)){return
}function x(){var A;
if(v.parent().hasClass("s9ShovelerCell")){A=v.parent().width()-y.width()
}else{A=v.get(0).offsetWidth-y.width()
}if(A<108){A=108
}if(A>950){A=950
}A+=t;
u.css("width",A)
}function h(){function C(){function D(G,F){if(G.widgetLeft!==F.widgetLeft){return false
}if(G.widgetTop!==F.widgetTop){return false
}if(G.containerLeft!==F.containerLeft){return false
}if(G.containerTop!==F.containerTop){return false
}return true
}var E={widgetLeft:Math.floor(v.offset().left),widgetTop:Math.floor(v.offset().top),containerLeft:Math.floor(g.parent().offset().left),containerTop:Math.floor(g.parent().offset().top)};
if(k===null||!D(E,k)){k=E;
return true
}return false
}if(u===null){return
}x();
u.css("height",j.height()+1);
if(C()===false){return
}var B=j.offset();
var A=g.offset();
u.css("left",B.left-A.left);
u.css("top",B.top-A.top)
}function l(){u=j.clone();
u.css({visibility:"visible",zoom:"1",display:"none","background-color":"white"});
h();
u.bind("mouseout",o);
u.bind("mouseover",q)
}function s(){i=setTimeout(function(){i=null;
h();
u.data("shown","false").data("beingShown","false");
u.children().fadeOut(m,function(){u.css("display","none")
})
},p)
}function z(){if(i){clearTimeout(i)
}}function n(){u.data("beingShown","true").data("shown","false");
var A;
if(u.css("display")==="none"){A=m;
u.children().css({opacity:0,display:"block"});
u.css({display:"block"})
}else{A=(1-u.children().css("opacity"))*m
}u.children().stop(true,false).fadeTo(A,1,function(){u.data("shown","true").data("beingShown","false");
g.children().not(f).hide().data("shown","false").data("beingShown","false");
h();
u.children().css("opacity","")
})
}function q(){z();
if(u===null){l();
u.appendTo(g)
}f=u;
w();
h();
if(u.data("beingShown")==="true"){return false
}if(u.data("shown")==="true"){return false
}n();
return false
}function o(){z();
s();
return false
}function w(){v.get(0).onmouseover=q;
v.get(0).onmouseout=o;
if(r===v&&v.parent().hasClass("s9ShovelerCell")){r=v.parent();
r.css("background-color","white");
r.mouseover(function(){b(this).children(".asin").get(0).onmouseover()
});
r.mouseout(function(){b(this).children(".asin").get(0).onmouseout()
})
}}r.css("background-color","white");
w()
})
});
amznJQ.declareAvailable("s9Multipack")
})(jQuery)
});