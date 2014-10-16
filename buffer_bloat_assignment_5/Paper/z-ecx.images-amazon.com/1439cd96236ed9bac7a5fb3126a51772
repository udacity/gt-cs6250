var amz_taf_triggers={};var amz_taf_popoverOpened=false;var amz_taf_showSwfCalled=false;amznJQ.available("JQuery",function(){(function($){if(typeof($.amz_taf_getTwisterHandlers)!="undefined")return;var getSelectedVariant=function(dpState){return dpState['selected_variation_values'];}
var getSelectedDimensions=function(variationValues){if(!variationValues)return null;var validKeys=[];var noOfDimensions=0;for(var dimension in variationValues){noOfDimensions++;if(typeof(variationValues[dimension])!="undefined"&&variationValues[dimension]!=-1){validKeys[validKeys.length]=dimension;}}
if(validKeys.length==noOfDimensions)return null;return validKeys;}
var selectedASIN=null;var getAsinFromVariant=function(asinVariations,selectedVariant,validKeys){if(!asinVariations||!selectedVariant||!validKeys){return null;}
for(var obj in asinVariations){var valid=true;for(var j=0;j<validKeys.length;j++){if(!asinVariations[obj][validKeys[j]]){continue;}
if(asinVariations[obj][validKeys[j]]!=selectedVariant[validKeys[j]]){valid=false;break;}}
if(valid){selectedASIN=asinVariations[obj]["ASIN"];return true;}}
return false;}
var isAlreadySelected=function(validKeys,selectedVariant,variations){if(!selectedASIN||!variations)return false;for(var i=0;i<validKeys.length;i++){if(variations[selectedASIN][validKeys[i]]!=selectedVariant[validKeys[i]])return false;}
return true;}
var updateHrefs=function(elementId){var element=jQuery('#'+elementId);var href=jQuery(element).attr('href');if(selectedASIN){if(href.indexOf("childASIN")>=0){href=href.replace(/childASIN=.*/g,"childASIN="+selectedASIN);}else{href+="&childASIN="+selectedASIN;}}
if(parentASIN){if(href.indexOf("parentASIN")>=0){href=href.replace(/parentASIN=[^\&]*/g,"parentASIN="+parentASIN);}else{href+="&parentASIN="+parentASIN;}}
jQuery(element).attr('href',href);}
var updateSocialNetworkLinks=function(elementId){var element=jQuery('#'+elementId);var socialButtons=jQuery(element).parent().find('.tafSocialButton').parent();for(var i=0;i<socialButtons.length;i++){var socialButton=jQuery(socialButtons[i]);var href=socialButton.attr('href');href=href.replace(/%2Fdp%2F[^\/%]*%2Fref/g,"%2Fdp%2F"+selectedASIN+"%2Fref");var onClick=socialButton.attr('onClick');if(onClick&&!onClick.replace){if(socialButton.length>0&&socialButtons[i].getAttributeNode){if(socialButtons[i].getAttributeNode('oldOnClick')){onClick=socialButtons[i].getAttributeNode('oldOnClick').value;}else if(socialButtons[i].getAttributeNode('onClick')){onClick=socialButtons[i].getAttributeNode('onClick').value;}
if(onClick&&onClick.replace&&onClick!="null"){onClick=onClick.replace(/%2Fdp%2F[^%\/]*%2Fref/g,"%2Fdp%2F"+selectedASIN+"%2Fref");socialButton.unbind('click');socialButtons[i].setAttribute('oldOnClick',onClick);onClick=new Function(onClick);socialButtons[i].onclick=onClick;}}}else if(onClick){onClick=onClick.replace(/%2Fdp%2F[^%\/]*%2Fref/g,"%2Fdp%2F"+selectedASIN+"%2Fref");socialButton.unbind('click');socialButton.attr('onClick',onClick);}
socialButton.attr('href',href);}
}
var updateEventsForShare=function(){for(triggerID in amz_taf_triggers){amz_taf_bindLightBoxTrigger(triggerID,selectedASIN,parentASIN);updateHrefs(triggerID);updateSocialNetworkLinks(triggerID);if(amz_taf_triggers&&amz_taf_triggers[triggerID]&&amz_taf_triggers[triggerID].isCompact){jQuery('#'+triggerID).removeAmazonPopoverTrigger();amz_taf_bindCompactPopoverTrigger(triggerID);}
}}
var asin_deselect=function(dpState){var selectedVariant=getSelectedVariant(dpState);var validKeys=getSelectedDimensions(selectedVariant);if(validKeys==null)return;if(isAlreadySelected(validKeys,selectedVariant,dpState['asin_variation_values'])){return;}
if(!getAsinFromVariant(dpState['asin_variation_values'],selectedVariant,validKeys)){return;}
if(dpState['parent_asin']){parentASIN=dpState['parent_asin'];}
updateEventsForShare();}
var document_ready=function(dpState){var selectedVariant=getSelectedVariant(dpState);var validKeys=getSelectedDimensions(selectedVariant);if(validKeys==null)return;if(isAlreadySelected(validKeys,selectedVariant,dpState['asin_variation_values'])){return;}
if(!getAsinFromVariant(dpState['asin_variation_values'],selectedVariant,validKeys)){return;}
updateEventsForShare();}
$.amz_taf_getTwisterHandlers=function(event_type){if(event_type=="asin_deselect")return asin_deselect;if(event_type=="document_ready")return document_ready;}
var twisterInitialized=false;$.amz_taf_initTwisterHandler=function(){if(twisterInitialized)return;amznJQ.available("twister",function(){if(!DetailPageFramework||!DetailPageFramework.registerCallback){return;}
DetailPageFramework.registerFeatureConfig("_tell_a_friend",{suppressDefaultBehaviour:true,dataType:'btf'});DetailPageFramework.registerCallback("asin_deselect","_tell_a_friend",jQuery.amz_taf_getTwisterHandlers("asin_deselect"));});twisterInitialized=true;}})(jQuery);});function amz_taf_generatePopover(triggerID,useTwister){var hashValue=window.location.hash;var hashIndex;var swfHashValue="_"+triggerID+"_Swf";var isRedirect=false;hashIndex=hashValue.indexOf(swfHashValue);if(hashValue!=""&&hashIndex>-1){isRedirect=true;}
var url=window.location.pathname;url+=window.location.search;if(window.location.hash&&window.location.hash!=""&&window.location.hash!="#"){var hash=window.location.hash.replace(/_[^&?/]*_Swf/,"");url+=hash;}
if(!isRedirect){if(url.indexOf("#")>-1){url+="&"+swfHashValue;}else{url+="#"+swfHashValue;}}
if(encodeURIComponent){url=encodeURIComponent(url);}else if(encodeURI){url=encodeURI(url);}else{url=escape(url);}
amz_taf_triggers[triggerID].url=amz_taf_triggers[triggerID].url+"&redirectLocation="+url;amz_taf_triggers[triggerID].origTriggerID=triggerID;var isCompact=amz_taf_triggers[triggerID].isCompact;amz_taf_bindLightBoxTrigger(triggerID);if(isCompact){amz_taf_bindCompactPopoverTrigger(triggerID);}
if(isRedirect&&!amz_taf_showSwfCalled){amz_taf_showSwfCalled=true;jQuery("#"+triggerID).trigger('click');}
if(useTwister){jQuery.amz_taf_initTwisterHandler();}}
function amz_taf_bindCallbacks(eventName,fn){if(amz_taf_generatePopover.handler=='undefined')amz_taf_generatePopover.handler={};jQuery(amz_taf_generatePopover.handlers).bind(eventName,fn);}
function amz_taf_callEventHandlers(eventName,element){if(amz_taf_generatePopover.handler=='undefined')return;jQuery(amz_taf_generatePopover.handlers).trigger(eventName,[eventName,jQuery(element).attr("href")]);}
function amz_taf_bindLightBoxTrigger(triggerID,childASIN,parentASIN){var url=amz_taf_triggers[triggerID].url;if(childASIN){url=url+"&childASIN="+childASIN;}
if(parentASIN){if(url.indexOf("parentASIN")>=0){url=url.replace(/parentASIN=[^\&]*/g,"parentASIN="+parentASIN);}else{url+="&parentASIN="+parentASIN;}}
jQuery("#"+triggerID).removeAmazonPopoverTrigger();jQuery("#"+triggerID).amazonPopoverTrigger({title:'<span class="n2"><span style="position: relative;z-index: 100;padding: 10px 18px 18px 18px;font-size: 1em;"><span style="margin: 4px 0 4px 0; font-size: 1.15em;font-weight: bold;">'+amz_taf_triggers[triggerID].title+'</span></span></span>',cacheable:false,destination:url,location:"centered",width:530,closeText:amz_taf_triggers[triggerID].closeText,group:'taf',onShow:amz_taf_onShow,onHide:function(){if(amz_taf_triggers[triggerID]["origTriggerID"]){var actualTrigger=amz_taf_triggers[triggerID]["origTriggerID"];if(amz_taf_triggers[actualTrigger]["isCompact"]){amz_taf_bindLightBoxTrigger(actualTrigger);amz_taf_bindCompactPopoverTrigger(actualTrigger);}}},closeEventExclude:'CLICK_TRIGGER'});jQuery("#"+triggerID+"_img").click(function(){jQuery("#"+triggerID).trigger('click');return false;});}
function amz_taf_compactClick(triggerID){jQuery("#"+triggerID).click();return false;}
function amz_taf_bindCompactPopoverTrigger(triggerID){var socialNetworks=amz_taf_triggers[triggerID].socialNetworks;var contentHeight=socialNetworks.length*30-8-19-7;var upMargin=contentHeight+8+(19-9);var popoverHTML='<div align="left" id="tafCompact_'+triggerID+'" class="tafCompactPop">'
+'<div id="tafPopTopArrow" style="position:absolute;right:28px;top:-29px;height:10px;">'
+'<span class="tafSwfPoTopArrow"></span></div>'
+'<div id="tafPopDummy" style="height:'+contentHeight+'px;">&nbsp;</div>'
+'<div id="tafPopContent" style="position:absolute;margin:-'+upMargin+'px -17px;z-index:1000;">'
+'<ul style="list-style-type:none;margin:0px;padding:0px;">';var border="border-bottom:1px Solid #C9E1F4;";for(var i=0;i<socialNetworks.length;i++){var network=socialNetworks[i];if(network.isEmail){popoverHTML+="<li style='padding:6px 9px;margin:0px !important;font-size:11px;line-height:16px;"+border+"'>";var networkHTML=network.image+"<span class='tafShareText vam'>"+network.text+"</span>";popoverHTML+="<a href='"+network.url
+"' target='_blank' onclick='amz_taf_compactClick(\""+triggerID+"\");return false;'>"
+networkHTML+"</a>";popoverHTML+="</li>";}else{if(i==socialNetworks.length-1){border="none";}
popoverHTML+="<li style='padding:6px 9px;margin:0px !important;font-size:11px;line-height:16px;"+border+"'>";var networkHTML="<span class=' vam "+network.className
+"' style='"+network.style
+";margin:0px !important;'></span><span class='tafShareText vam' style='margin:0px;'>"
+network.text+"</span>";var networkOnClick=" onclick='window.open(this.href, \"_blank\", \"location=yes,width=700,height=400\");return false;'";if(network.newWindow)networkOnClick="";popoverHTML+="<a href='"+network.url+"' target='_blank' "+networkOnClick+">"+networkHTML+"</a>";popoverHTML+="</li>";}}
popoverHTML+="</ul></div></div>"
jQuery("#"+triggerID).unbind('click',amz_taf_noop);var compactPOParams={literalContent:popoverHTML,showOnHover:true,cacheable:false,hoverShowDelay:50,followLink:true,location:'bottom',locationMargin:12,align:'right',width:134,hoverHideDelay:300,showCloseButton:false,closeEventInclude:'CLICK_TRIGGER',group:'taf'};jQuery("#"+triggerID).amazonPopoverTrigger(compactPOParams);jQuery("#"+triggerID+"_img").amazonPopoverTrigger(compactPOParams);}
function amz_taf_noop(){return false;}
function amz_taf_unbindCompactPopoverTrigger(triggerID){jQuery("#"+triggerID).removeAmazonPopoverTrigger();jQuery("#"+triggerID+"_img").removeAmazonPopoverTrigger();jQuery("#"+triggerID).click(amz_taf_noop);}
function amz_taf_updatePopoverTarget(triggerID,newParams){var url=amz_taf_triggers[triggerID].url;if(newParams){url+='&';jQuery.each(newParams,function(key,val){url=url.replace(new RegExp(key+"=(:?.*?)&"),key+"="+escape(val)+'&');});amz_taf_triggers[triggerID].url=url.substr(0,url.length-1);}
jQuery("#"+triggerID).removeAmazonPopoverTrigger();amz_taf_generatePopover(triggerID);}
function amz_taf_validateRecipients(src){var recipients=jQuery.trim(src.value);recipients=recipients.split(/[,;\s]+/);var unique={};for(var i in recipients){unique[recipients[i]]=1;}
var invalid=new Array();for(var i=0;i<unique.length;i++){var e=unique[i];if(!e.match(/((?:[\w\.+-]*?[a-zA-Z0-9+])?@(?:[a-zA-Z0-9][\w-]*\.)+[a-zA-Z]{2,4})(.*)/)){invalid.push(e);}}
return invalid;}
function amz_taf_validateMessage(src){var message=src.value;var re=/[\r]/g;message=message.replace(re,"");var maxLength=amz_taf_config.maxLength;var messageLength=message.length;var charsLeft=maxLength-messageLength;var rulesObj=document.getElementById("taf_send_message_rules");var rulesErrorObj=document.getElementById("taf_send_message_rules_error");if(!rulesObj||!rulesErrorObj)
return true;var charsLeftObj="taf_msg_charsLeft";var pluralObj="taf_msg_plural";var isError=charsLeft<0;if(!isError){rulesObj.style.display='';rulesErrorObj.style.display='none';}else{rulesObj.style.display='none';rulesErrorObj.style.display='';charsLeftObj+="_error";pluralObj+="_error";charsLeft=-charsLeft;}
charsLeftObj=document.getElementById(charsLeftObj);pluralObj=document.getElementById(pluralObj);if(!charsLeftObj){return!isError;}
charsLeftObj.innerHTML=charsLeft;if(!pluralObj)return!isError;pluralObj.innerHTML=(charsLeft==1)?'':'s';return!isError;}
function amz_taf_textarea_onfocus(txt,defaultText){if(txt&&txt.value==defaultText){txt.value='';txt.style['color']='#000000';}}
function amz_taf_textarea_onblur(txt,defaultText){if(txt&&txt.value==''){txt.value=defaultText;txt.style['color']='#666666';}}
function amz_taf_textfield_onfocus(txt,defaultText){if(txt&&txt.value==defaultText){txt.value='';txt.style['color']='#000000';}}
function amz_taf_textfield_onblur(txt,defaultText){if(txt&&txt.value==''){txt.value=defaultText;txt.style['color']='#666666';}}
var amz_taf_popover;function amz_taf_onShow(popover){var triggerID=this.attr('id');if(typeof(amz_taf_config)!="undefined"){if(typeof(amz_taf_config[triggerID])!="undefined"){amz_taf_config=amz_taf_config[triggerID];}}
amz_taf_popover=popover;amz_taf_popover.processing=0;jQuery(document).keyup(function(evt){if(27==evt.which&&amz_taf_popover.css('visibility')!='hidden'&&amz_taf_popover.css('display')!='none'){amz_taf_popover.hide();}});if(amz_taf_triggers[triggerID]["isCompact"]){amz_taf_unbindCompactPopoverTrigger(amz_taf_triggers[triggerID].origTriggerID);}}
function amz_taf_sendDoneCallback(data){jQuery('.ap_content',amz_taf_popover).html(data);if(jQuery('#swfSuccessBox').length>0){setTimeout(function(){if(jQuery.browser.msie){setTimeout(function(){jQuery('div.ap_close',amz_taf_popover).click();},1000);}else{jQuery('.ap_popover').fadeOut(1000,function(){jQuery('div.ap_close',amz_taf_popover).click();});}},1000);}
if(jQuery('#swfCaptchaFields').length>0){var newTop=jQuery('.ap_popover').position().top-100;if(amz_taf_popover.captchaShown!=1){jQuery('.ap_popover').css({top:newTop});amz_taf_popover.captchaShown=1;}}
amz_taf_popover.processing=0;amz_taf_callEventHandlers("track_share_email");}
function amz_taf_sendButton_onSubmit(form){if(amz_taf_popover.processing){return false;}else{amz_taf_popover.processing=1;}
var friendsArr=document.getElementsByName('friendsRecipients');var recipientsObj=form.recipients;if(!friendsArr||!recipientsObj){return false;}
var postContent={};var count=0;var recipients=recipientsObj.value;if(recipients!=amz_taf_config.detailedInstructions){recipients=recipients.replace(/[,;]\s*/g,", ");recipients=recipients.replace(/^(,|;|\s)+/,"");recipients=recipients.replace(/(,|;|\s)+$/,"");if(recipients!=""){postContent.recipients=recipients;}}
var selectedFriends=[];for(var i=0;i<friendsArr.length;i++){if(friendsArr[i].checked){selectedFriends.push(friendsArr[i].value);count++;}}
if(selectedFriends.length>0){postContent.friendsRecipients=selectedFriends;}
if(form.message&&form.message.value.length>0&&form.message.value!=amz_taf_config.messageInstructions){postContent.message=form.message.value;}
if(form.copyMeBox.checked){postContent.copyMeBox="on";}
if(form.inviteBox&&form.inviteBox.checked){postContent.inviteBox="on";}
var fields={ces:1,contentID:1,contentName:1,contentType:1,contentURI:1,emailTemplate:1,guess:1,imageURL:1,params:1,placementID:1,titleText:1,channel:1,eventID:1,params:1,merchantID:1,viaAccount:1,relatedAccounts:1,parentASIN:1,isDynamicSWF:1,emailSubjectStrID:1,emailCustomMsgStrID:1,learnMoreButton:1,emailCaptionStrID:1,emailDescStrID:1,__mk_ja_JP:1,__mk_de_DE:1,__mk_fr_FR:1,__mk_zh_CN:1,referer:1};for(var field in fields){if(fields.hasOwnProperty(field)&&typeof form[field]!=='undefined'){postContent[field]=form[field].value;}}
postContent.token=form.token.value;jQuery.post(amz_taf_config.link(count),postContent,amz_taf_sendDoneCallback);return false;}
function amz_taf_postPopOverSetup(){(function($){$('#swfPopCloseButton').click(function(){$('div.ap_close',amz_taf_popover).click();});$('#swfSubmitButton').click(function(){var form=$('form[name="tellAFriendForm"]');var recipients=form.find('textarea[name="recipients"]')[0];if(recipients.value==amz_taf_config.detailedInstructions){$('#swf_error_box_text').html(amz_taf_config.noRecipient);$('#swf_error_box').show();return false;}
var invalid=amz_taf_validateRecipients(recipients);if(invalid.length>0){var error=amz_taf_config.badAddress;error+=' '+invalid.join(', ');$('#swf_error_box_text').html(error);$('#swf_error_box').show();return false;}
var msg=form.find('textarea[name="message"]')[0];if(msg&&!amz_taf_validateMessage(msg)){$('#swf_error_box_text').html(amz_taf_config.sendError);$('#swf_error_box').show();return false;}
var guess=form.find('input[name="guess"]')[0];if(guess&&guess.value==amz_taf_config.guessMsg){$('#swf_captcha_error_box_text').html(amz_taf_config.noCaptchaGuess);$('#swf_captcha_error_box').show();return false;}
$('form[name="tellAFriendForm"] input:hidden[name="channel"]').val('email');amz_taf_sendButton_onSubmit($('.tafPoContent form')[0]);});$('form[name="tellAFriendForm"]').submit(function(){$(this).find('input:hidden[name="channel"]').val('email');amz_taf_sendButton_onSubmit(this);return false;});$('.socialnet').bind("click",function(event){amz_taf_callEventHandlers("update_popover",this);return false;});$('.tafSocialLink').bind("click",function(event){amz_taf_callEventHandlers("update_popover",this);return false;});})(jQuery);};amznJQ.declareAvailable('share-with-friends-js-new');