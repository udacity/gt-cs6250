window.S9AivPopover={};
if(typeof amznJQ!=="undefined"){amznJQ.onReady("jQuery",function(){amznJQ.onReady("popover",function(){(function(a){if(a.browser.msie&&a.browser.version.indexOf("6")===0){return
}jQuery(".s9AivPopover").each(function(c,d){var b=a(d);
b.parent().removeAttr("title");
b.amazonPopoverTrigger({showOnHover:true,hoverHideDelay:0,width:295,hoverShowDelay:400,followLink:true,destination:"/gp/video/watchlist/ajax/hoverbubble.html?page=s9-hover&reftagPrefix=s9_&ASIN="+b.attr("id"),cacheable:false,loadingContent:'<span class="spinner">LOADING</span>',location:function(i,g){var f=a("img",this),e=jQuery(window).width(),l=f.width(),n=f.offset().left,m=f.offset().top;
var k=(e-(n+l)),h=n;
var j;
if(k<300){if(h<300){j=h<=k
}else{j=false
}}else{j=true
}if(j){n=n+l;
jQuery(".watchlist-arrow").attr("class","watchlist-arrow-Left")
}else{n=n-300;
jQuery(".watchlist-arrow").attr("class","watchlist-arrow-Right")
}return{left:n,top:m}
},skin:function(){return'<div class="s9Popover"><div class="watchlist-popover"><div class="watchlist-popover-top"></div><div class="watchlist-popover-body"><div class="watchlist-arrow"><div class="ap_title"></div><div class="ap_content"></div></div><div class="amzn-logo"></div></div><div class="watchlist-popover-bottom"></div></div></div>'
}})
})
})(jQuery)
})
})
};