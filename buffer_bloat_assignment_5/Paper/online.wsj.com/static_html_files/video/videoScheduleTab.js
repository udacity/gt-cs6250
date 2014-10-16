dj.module.video.videoTab = {
	init: function(){
		this.player = null;
		dojo.connect(dojo.byId('vcrTab_tab_Video'),"onclick",this, function(ev){
			var cb=new Date().getTime();
			var url="/api-video/find_all_videos.asp?cb="+cb+"&type=column&query=What's+News&count=1&fields=id,name,description,wsj-section,wsj-subsection,linkURL,column";
			var that = this;
			dojo.xhrGet({
 				url      : url,
 				handleAs : "json",
 				load     : function(response, ioArgs) {
 					var guid = response.items[0].id;
 					var spanId = dojo.byId('videoHint');
 					that.dataset = {guid: guid, videoSize:"E"}; 
 					if(spanId){
 						that.playVideo(response);
 					}else if (dojo.byId('player').getAttribute('data-id')==guid && !dj.module.videos.liveVideoSchedule.isScheduledPlay){
 						var pid = "whatsNewsVideoPlayer&clickForSound=";
 						if(swfobject.getObjectById(pid+"true")){
							swfobject.getObjectById(pid+"true").unpauseVideo();
						}else if(swfobject.getObjectById(pid+"false")){
							swfobject.getObjectById(pid+"false").unpauseVideo();
						}
						console.log("UNPAUSE VIDEO");
 					}else{
 						that.playVideo(response);
 					}
 					dojo.byId('player').setAttribute('data-id',guid);
 				}
			});
		});
		dojo.connect(dojo.byId('vcrTab_tab_Schedule'),"onclick",function(){
			var id = "whatsNewsVideoPlayer&clickForSound=";
			if(swfobject.getObjectById(id+"true")){
				swfobject.getObjectById(id+"true").pauseVideo();
			}else if(swfobject.getObjectById(id+"false")){
				swfobject.getObjectById(id+"false").pauseVideo();
			}else{
				swfobject.getObjectById("whatsNewsVideoPlayer").pauseVideo();

			}
			dj.module.videos.liveVideoSchedule.isScheduledPlay=false;
			console.log("PAUSE VIDEO");
		});
	},
	playVideo : function(response){
		var bid = "whatsNewsVideoPlayer&clickForSound="
		var id = bid+dj.module.videos.liveVideoSchedule.isScheduledPlay;
		var that = this;
		if(dojo.byId('whatsNewsVideoPlayer')){
			dojo.byId('whatsNewsVideoPlayer').id=id;
		}else if(dojo.byId(bid+'true')){
			dojo.byId(bid+'true').id=id;
		}else if(dojo.byId(bid+'false')){
			dojo.byId(bid+'false').id=id;
		}
		this.player = new dj.widget.video.MicroPlayer(id, this.dataset);
		this.player.loadVideo();
		console.log("PLAY VIDEO");
		this.player.controller.subscribeByName(this.player.controller._events.stopVideo, function() { 
			dojo.byId('vcrTab_tab_Schedule').click();
			dj.module.videos.liveVideoSchedule.isScheduledPlay = false;
			swfobject.getObjectById(id).pauseVideo();
			console.log("STOPPED");
		});
		this.player.controller.observer.subscribeByName(this.player.controller._events.continueLoadVideo, function() {
			var linkURL = that.player.controller.videoInformation.linkURL;
			var titleURL = "<a href='"+linkURL+"'>";
			var ri=response.items[0];
			dojo.query('#wnVideoDesc > h2')[0].innerHTML = titleURL+ri.name;
			dojo.byId('wnDesc').innerHTML=ri.description;
			console.log("LOADED VIDEO");
		}, this);
	}
};
