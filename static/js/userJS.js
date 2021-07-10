$(document).ready(function(){
	
	function slideImages( imgNo ){
		setTimeout( function(){
			$("#imageSlider img, #imageSlider label").fadeOut( 300, function(){
				$("#imageSlider img").attr('src', 'sampleSlideImages/'+imgNo+'.jpg').fadeIn( 500 );
				$("#imageSlider label").html( imgTextArr[ Number(imgNo) - 1 ] );
				setTimeout( function(){
					$("#imageSlider label").fadeIn( 300 );//.animate({marginLeft: '-=1%'}, 1000);
				}, 2000 );
			});
			imgNo++;
			slideImages( imgNo );
			if( Number(imgNo) == 10 ){
				imgNo = 9;
				slideImages( imgNo );
			}
		}, 10000);
	}
	imgNo = 0;
	slideImages(imgNo);

	var imgTextArr = ["A <span>Place</span> to impart <span>life values</span> along with <span>technical education</span>", "A <span>Role Model</span> To Follow", "<span>Progressive Placements</span>", "Awarded as <span>2nd e-Governance campus</span>", "A Place for <span>Recreation</span> and <span>Entertainment</span>", "<span>2nd International Conference</span> Held in March 2016", "<span>Eco - Friendly</span> Campus", "<span>Interactive Lecturing</span>", "Practical Learning", "Need To Decide", "Need To Decide"];

	$("#imageSlider a").click( function(){
			splitUrl = $("#imageSlider img").attr('src').split('/');
			extSplit = splitUrl[splitUrl.length - 1].split('.');
			if( $(this).attr('class') == 'prev' ){
				if( extSplit[0] > 1 ){
					$("#imageSlider img").fadeOut( 500, function(){
					$("#imageSlider img").attr( 'src', 'sampleSlideImages/'+(Number(extSplit[0])-Number(1))+'.jpg' ).fadeIn( 500 );
					$("#imageSlider label").html(imgTextArr[(Number(extSplit[0]))]);
				});
			}
		}
			else if( $(this).attr('class') == 'next' ){
				if( extSplit[0] < 9 ){
					$("#imageSlider img").fadeOut( 500, function(){
					$("#imageSlider img").attr( 'src', 'sampleSlideImages/'+(Number(extSplit[0])+Number(1))+'.jpg' ).fadeIn( 500 );
					$("#imageSlider label").html(imgTextArr[(Number(extSplit[0]))]);
				});
			}
		}
	});

	//$("#photoLightBox").css();

	$("#photoLightBox").css({'top':$("#alumni").position().top - Number(140)});

	$("#photoLightBox").dblclick(function(){
		$(this).fadeOut( 500 );
		$("body").css('overflow','auto');
	});

	$("#alumni #aboutAlumnus").click( function() {
		window.location = 'Alumnus';
	});

//	var backUrl = window.location.search;
//	splitBackUrl = backUrl.split('=');
//	setTimeout( function(){
//		$("html, body").animate({scrollTop: $("#"+splitBackUrl[1]).offset().top - Number(130)}, 2000);
//		$("#collegeBanner").fadeOut( 300, function(){
//			$("#homeCollegeBanner").fadeIn( 300 );
//		});
//	}, 100);
//
	$("#placements #acaYearSel option:nth-child(2)").attr( 'selected','selected' );

	$("#placements #acaYearSel").change( function(){
		if( window.XMLHttpRequest ){
			var xmlhttp = new XMLHttpRequest();
		}
		else {
			var xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
		}
		xmlhttp.onreadystatechange = function(){
			if( xmlhttp.readyState == 4 && xmlhttp.status == 200 ){
				splitRows = xmlhttp.responseText.split(';');
				selStudents = splitRows[0].split('=');
				compVisits = splitRows[1].split('=');
				$(".selectedStudents #circle").html( selStudents[1] ).fadeIn( 300 );
				$(".compVisited #circle").html( compVisits[1] ).fadeIn( 300 );
			}
		}
		xmlhttp.open('POST', 'getPlacementsData.php', true);
		xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xmlhttp.send('acaYear='+$(this).val());
	});

	$(document).on('click', '#dispContent h3 span', function(){
	thisMainDivId = $(this).closest('div').attr('id');
		if($(this).text() == '-'){
			$("#"+thisMainDivId+' #data').slideUp( 300 );
			$(this).text('+');
		}
		else if($(this).text() == '+'){
			$("#"+thisMainDivId+' #data').slideDown( 300 );
			$(this).text('-');
		}
	});

	$("#aboutSrit a").click( function(){
		thisBg = $(this).css('background');
		if( thisBg.substr(0, 16)  == 'rgba(0, 0, 0, 0' ){
			$("#aboutSrit a").css( {'background':'linear-gradient(#FB8E43,#FF7110)', 'color':'#FFF', 'border-color':'transparent', 'margin-top':'0'} );
			$(this).css( {'background':'#FFF', 'font-weight':'bold', 'color':'#FF7110', 'border-color':'#FF7110'} );
		}
	});

	function commonXMLHTTP(divName, fileName, data){
		if(window.XMLHttpRequest){
			xmlhttp = new XMLHttpRequest();
		}
		else{
			xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
		}
		xmlhttp.onreadystatechange = function(){
			if(xmlhttp.readyState = 4 && xmlhttp.status == 200){
				//document.getElementById( divName ).innerHTML = xmlhttp.responseText;
			$("#"+divName).html(xmlhttp.responseText).css('display', 'block');
			//alert(xmlhttp.responseText);
				return $("#"+divName).html();
			}
		}
		if(data != ''){
			xmlhttp.open('POST', fileName, true);
			xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
			xmlhttp.send(data);
		}
		else{
			xmlhttp.open("GET", fileName, true);
			xmlhttp.send();
		}
	}

	$("#aboutMenus label").click(function(){
		thisText = $(this).find('span').text();
		divName = 'dispContent';
		fileName = 'getAboutSrit.php';
		data = 'topicName='+thisText;
		commonXMLHTTP(divName, fileName, data);
	});

	$("#aboutSrit #aboutMenus label").click(function(){
		thisBg = $(this).css('background');
				if( thisBg.substr(0, 16)  == 'rgba(0, 0, 0, 0)' ){
			$("#aboutSrit a").css( {'background':'linear-gradient(#FB8E43,#FF7110)', 'color':'#FFF', 'border-color':'transparent', 'margin-top':'0'} );
			$(this).css( {'background':'#FFF', 'font-weight':'bold', 'color':'#FF7110', 'border-color':'#FF7110'} );
		}
	});

	$("#address label img").click( function(){
		window.open($(this).attr('href'), '_blank');
	});

	$("section").mouseenter( function(){
		$("#menus a").css({'background':'transparent', 'color':'#505050'});
		$("#menus a."+$(this).attr('id')).css({'background':'#FF7110', 'color':'#FFF'});
	});

	$("#placements #overAllProgress #circle").click( function(){
		window.location="placements/";
	});

	$("#departments #departments_sub #department").click( function(){
		window.location="departments/"+$(this).attr('class');
	});

	$("#facilities #facilitys #fac").click( function(){
		window.location = 'Facilities/?clicked='+$(this).attr('class');
	});

	$("#collegeBanner #menus a, #homeCollegeBanner #menus a").click( function(){
		thisClass = '';
		thisClass = $(this).attr('class');
		if( thisClass == 'home' ){
			$("html, body").animate({scrollTop: $("body").offset().top - Number(133)}, 2000);
			$("#homeCollegeBanner").fadeOut( 500, function(){
				$("#collegeBanner").fadeIn( 500 );
			});
		}
		$("#menus a").css({'background':'transparent', 'color':'#000'});
		$(this).css({'background':'#FF7110', 'color':'#FFF'});
		$("html, body").animate({scrollTop: $("#"+$(this).attr('class')).offset().top - Number(130)}, 2000);
		$("#collegeBanner").fadeOut( 300, function(){
			$("#homeCollegeBanner").fadeIn( 300 );
		});
	});

		if( $("#imageSlider:hover").length == 1 ){
			$("#homeCollgeBanner").fadeOut( 300, function(){
				$("#collegeBanner").fadeIn( 300 );
			});
		}

	$("img#topBottNav").click( function(){
		if( $(this).attr('value') == 'top' ){
			$("html, body").animate({scrollTop: $("body").offset().top - Number(130)}, 1000);
			$(this).fadeOut( 300, function(){
				$(".bottDir").fadeIn( 300 );
			});
			$("#homeCollegeBanner").fadeOut( 500, function(){
				$("#collegeBanner").fadeIn( 500 );
			});
		}
		else if( $(this).attr('value') == 'bottom' ){
			$("html, body").animate({scrollTop: $("#footer").offset().top - Number(130)}, 1000);
			$(this).fadeOut( 300, function(){
				$(".topDir").fadeIn( 300 );
			});
		}
	});

	$("#alumni #aluAcaYears label").click( function(){
		thisText = $(this).text();
		if( window.XMLHttpRequest ){
			var xmlhttp = new XMLHttpRequest();
		}
		else{
			var xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
		}
		xmlhttp.onreadystatechange = function(){
			if( xmlhttp.readyState == 4 && xmlhttp.status == 200 ){
				divide = xmlhttp.responseText.split('SPLITTED');
				image_gal = '';
				divided_0 = divide[0].split(',');
				for(i=0; i < divided_0.length - 1; i++){
					if(divided_0[i] != ''){
						image_gal += '<img src="'+thisText+'/'+divided_0[i]+'.jpg">';
					}
				}
				$("#alumni #alumniHeading").text( ' Alumni Year '+thisText );
				$("#alumni #aluMsgData p").html(divide[1]);
			}
			$("#alumni #aluPhotoGallery").html(image_gal);
		}
		xmlhttp.open('POST', 'getAlumniData.php', true);
		xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xmlhttp.send( 'aluAcaYear='+$(this).text() );
	});

	$("#newsSRIT #newsDescription #news").click( function(){
		thisNewsClass = $(this).attr('class');
		$("#newsLightBox #clickedDiv p").html($("#newsSRIT ."+thisNewsClass+" p").text());
		thisNewsImg = '';
		if( $("#newsSRIT #newsDescription ."+thisNewsClass+' img').is(':visible') ){
			thisNewsImg = $("#newsSRIT ."+thisNewsClass+" img").attr('src').split('/');
			$("#newsLightBox #clickedDiv img").css({'display':'inline-block'});
			thisNewsImgName = thisNewsImg[ thisNewsImg.length - 1 ].split('.');
			var thisNewsLarImg = $("#newsLightBox #clickedDiv img").attr('src' ,'NewsClips/'+thisNewsImgName[0]+'_large.jpg');
			setTimeout( function(){
				if( thisNewsLarImg.width() < thisNewsLarImg.height() ){
					$("#newsLightBox #Img").css({'width':'40%', 'display':'block', 'margin':'0 auto'});
				}
				else if( thisNewsLarImg.width() > thisNewsLarImg.height() ){
					$("#newsLightBox #Img").css({'width':'60%', 'display':'block', 'margin':'0 auto'});
				}
				$("#newsLightBox #clickedDiv img").attr('src' ,'NewsClips/'+thisNewsImgName[0]+'_large.jpg');
			}, 100 );
		}
		else {
			$("#newsLightBox #clickedDiv img").attr('src', 'NewsClips/altImg.png').css({'width':'60%', 'display':'block', 'margin':'0 auto'});
		}
		$("#newsSRIT #newsLightBox").fadeIn( 300 );
	});

	$("#newsLightBox #clickedDiv #close").click( function(){
		$("#newsLightBox").fadeOut( 500 );
		$("#newsLightBox img").attr('src', '');
		$("#newsLightBox p").text('');
	});

});

	// $(document).on('mouseenter', "#contactClick", function(){
	// 	$("#contactUs").fadeIn( 400 );
	// });
	// $(document).on('mouseleave', "#contactUs", function(){
	// 	$(this).slideUp( 500 );
	// });

	$(document).on('click', '#collegeBanner #logo, #homeCollegeBanner #logo').click( function(){
		window.location = '../';
	});

	$(document).on( 'click', '#sidePanel ul li', function(){
		if( window.XMLHttpRequest ){
			xmlhttp = new XMLHttpRequest();
		}
		else{
			xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
		}
		$("#head").text('Placements in '+ $(this).text() );
		xmlhttp.onreadystatechange = function(){
			if( xmlhttp.readyState == 4 && xmlhttp.status == 200 ){
				if( xmlhttp.responseText != 'false' ){
					splitRows = xmlhttp.responseText.split(';');
					data = '';
					$("#companyPanel table tbody").html('');
					for( i=0; i<splitRows.length; i++ ){
						splitCols = splitRows[i].split(',');
						if( splitCols.length > 1 ){
							$("#companyPanel table tbody:last").append('<tr></tr>');
						}
						for( j=0; j < splitCols.length; j++ ){
							data = data + '<td>'+splitCols[j]+'</td>';
						}
						$("#companyPanel table tbody tr:last").html('<td>'+(Number(i)+1)+'</td>'+data);
						data = '';
					}
				}
			}
		}
		data = 'acaYear='+$(this).text();
		xmlhttp.open('POST', 'getPlacedRecords.php', true);
		xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xmlhttp.send(data);
	});

	$(document).on('click', '#alumnniRegBut', function(){
		$("#container,#topTotalBanner").css({'-newkit-filter':'blur(3px)', 'overflow':'hidden'});
		$("#alumRegSec").fadeIn( 500 );
	});
	$(document).on('click', '#alumRegSec h2 span', function(){
		$("#alumRegSec").fadeOut( 500 );
		$("#container,#topTotalBanner").css({'-newkit-filter':'blur(0px)'});
	});

	var lastScroll = 0;
		$(window).scroll( function(e){
		var nowScroll = $(this).scrollTop();
		if( nowScroll > lastScroll ){
			if( $("#imageSlider:hover").length == 0 ){
				$("#collegeBanner").fadeOut( 500, function(){
					$("#homeCollegeBanner").fadeIn( 500 );
				} );
			}
		}
		else if( nowScroll < lastScroll ){
			if( $("#imageSlider:hover").length == 1 ){
				$("#homeCollegeBanner").fadeOut( 500, function(){
					$("#collegeBanner").fadeIn( 500 );
				} );
			}
		}
		lastScroll = nowScroll;
	} );

	$(document).on('mouseenter', '#admAca #service', function(){
		$("#admAca #service").css({'-newkit-filter':'blur(7px)'});
		$(this).css({'-newkit-filter':'blur(0px)'});
	} );
	$(document).on('mouseleave', '#admAca #service', function(){
		$("#admAca #service").css({'-newkit-filter':'blur(0px)'});
	} );

	$(document).on('click', '#admAca #service', function(){
		clicked = $(this).attr('class');
		window.location='academics/?clicked='+$(this).attr('class');
	});
	$(document).ready( function(){
				var url = window.location.search.substring(1);
				varSplit = url.split('=');
				setTimeout( function(){
					$("."+varSplit[1]).trigger( 'click' );
				}, 10);

				$("#address label img").click( function(){
					window.open($(this).attr('href'), '_blank');
				});

				$("#menu a").click( function(){
					window.location="#"+$(this).attr('id');
				} );
				$("section").mouseenter( function(){
						$("#menus a").css({'background':'transparent', 'color':'#505050'});
						$("#menus a."+$(this).attr('id')).css({'background':'#FF7110', 'color':'#FFF'});
				} );

				$("#examSec #tabs label").click( function(){
					thisId = $(this).attr('id');
					$("#examSec #tabs label").css('transform', 'scale(1)');
					$("#examSec #tabs label img, #examSec #tabs label span").css('opacity', '0.5');
					$("#"+thisId).css('transform','scale(1.1)');
					$("#examSec #tabs label#"+thisId+" img, #examSec #tabs label#"+thisId+" span").css({'opacity':'1'});
					$("#examSec #tabsInfo div").hide( 200, function(){
						$("."+thisId).fadeIn( 400 );
						if( thisId == 'not' ){
							imgName = 'noti_Back';
						}
						else if(thisId == 'exmTT'){
							imgName = 'examTT_Opa';
						}
						else if( thisId == 'res' ){
							imgName = 'res_Back';
						}
						$("#examSec #tabsInfo").css({'background':'url(images/'+imgName+'.png)', 'background-repeat':'no-repeat', 'background-position':'center center'});
					});
				});

			});

		/* $(document).ready( function(){
			function ajaxCall(thisId, dept){
				if(window.XMLHttpRequest){
					var xmlhttp = new XMLHttpRequest();
				}
				else{
					var xmlhttp = ActiveXObject('Microsoft.XMLHTTP');
				}
				xmlhttp.onreadystatechange = function(){
					if( xmlhttp.readyState == 4 && xmlhttp.status == 200 ){
						$("#departmentsPage #dispDeptInfo #display").html( xmlhttp.responseText );
					}
				}
				data = 'menuName='+thisId+'&deptName='+dept;
				xmlhttp.open('POST', 'showSideMenuInfo.php', true);
				xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
				xmlhttp.send(data);
			}
		}); */

		$(document).on("mouseenter", '#departmentsPage #deptInfo #facImages .empDet', function(){
			thisImgId = $(this).attr('id');
			$("#departmentsPage #deptInfo #facImages #"+thisImgId).next('div#layer').slideDown( 500 );
		});
		$(document).on("mouseleave", '#departmentsPage #deptInfo #facImages .empDet', function(){
			thisImgId = $(this).attr('id');
			$("#departmentsPage #deptInfo #facImages #"+thisImgId).next('div#layer').slideUp( 500 );
		});

	function ajaxCallFaclts( clickedOn ){
		if( window.XMLHttpRequest ){
			var xmlhttp = new XMLHttpRequest();
		}
		else {
			var xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
		}
		xmlhttp.onreadystatechange = function(){
			if( xmlhttp.readyState == 4 && xmlhttp.status == 200 ){
				$("#facilitiesMainPage #display").html(xmlhttp.responseText);
			}
		}
		xmlhttp.open('POST', '../Facilities/getFacilitiesDetails.php', true);
		xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xmlhttp.send('facName='+clickedOn);
	}
		var arrayQuotes = [];
		arrayQuotes["Library"] = "Without libraries what have we? We have no past and no future";
		arrayQuotes["Hostel"] = "The Second Home....";
		arrayQuotes["Transport"] = "Friendly Journey....";
		arrayQuotes["Wifi"] = "The Internet: Transforming the society and shaping the future.";
		arrayQuotes["Sports"] = "Every champion was once a contender that refused to give up.";

	$(document).on('click', '#facilitiesMainPage #aboutMenus label', function(){
		thisLabelClass = $(this).attr('class');
		$("#facilitiesMainPage .displayImg img").attr('src', '../images/'+thisLabelClass+'.jpg');
		$("#facilitiesMainPage .displayImg span").text(arrayQuotes[thisLabelClass]);
		ajaxCallFaclts( thisLabelClass );
	});

	$(document).on('click', '#collegeBannerSmall #menus a', function(){
		var url = window.location.href;
		splitUrl = url.split('/');
		if( splitUrl[splitUrl.length - 2] != 'new' ){
			if( splitUrl[splitUrl.length - 3] == 'departments' ){
				thisUrl = '.\.\clicked='+$(this).attr('class');
				window.location='../../?clicked='+$(this).attr('class');
			}
			else {
				window.location='../?clicked='+$(this).attr('class');
			}
		}
	});

	$(document).on('click', '#collegeBanner #logo, #collegeBannerSmall #logo, #homeCollegeBanner #logo', function(){
		window.location = '../';
	});

	function ajaxCall(thisId, dept){
		if(window.XMLHttpRequest){
			var xmlhttp = new XMLHttpRequest();
		}
		else{
			var xmlhttp = ActiveXObject('Microsoft.XMLHTTP');
		}
		xmlhttp.onreadystatechange = function(){
			if( xmlhttp.readyState == 4 && xmlhttp.status == 200 ){
				$("#departmentsPage #dispDeptInfo #display").html( xmlhttp.responseText );
			}
		}
		data = 'menuName='+thisId+'&deptName='+dept;
		xmlhttp.open('POST', 'showSideMenuInfo.php', true);
		xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xmlhttp.send(data);
	}

	var url = window.location.href;
	varSplit = url.split('/');

	$(document).on('click', '#departmentsPage #aboutMenus label', function(){
		window.location = '../'+$(this).attr('class');
	});

	$(document).on('click', "#departmentsPage #dispDeptInfo #sideMenus a.menu", function(){
		thisId = $(this).attr('id');
		ajaxCall(thisId, window.varSplit[window.varSplit.length - 2]);
	});

	function acaAjaxCall(clickedName, fileName, toDisplay){
		if( window.XMLHttpRequest ){
			var xmlhttp = new XMLHttpRequest();
		}
		else {
			var xmlhttp = ActiveXObject('Microsoft.XMLHTTP');
		}
		xmlhttp.onreadystatechange = function(){
			if( xmlhttp.readyState == 4 && xmlhttp.status == 200 ){
				$(toDisplay).html(xmlhttp.responseText);
			}
		}
		xmlhttp.open('POST', fileName, true);
		xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xmlhttp.send('clickedOn='+clickedName);
	}

		var url = window.location.search;
		splittedUrl = url.split('=');
		setTimeout( function(){
			$("#academicsPage #aboutMenus label."+splittedUrl[1]).trigger( 'click' );
		}, 100 );

		$(document).on('click', "#academicsPage #aboutMenus label", function(){
			clickedName = $(this).attr('class');
			fileName = 'getAcademicsInfo.php';
			toDisplay = "#academicsPage #display";
			acaAjaxCall(clickedName, fileName, toDisplay);
		});

	$(document).on('click', '#tabInfoDisp #tabs label', function(){
		clickedName = $(this).attr('id');
		fileName = 'examSecCallPage.php';
		toDisplay = "#academicsPage #display #tabsInfo";
		acaAjaxCall(clickedName, fileName, toDisplay);

	});

	$(document).on('click', "#academicsPage #aboutMenus label", function(){
		thisClass = $(this).attr('class');
		if( thisClass == 'examSec' ){
			setTimeout( 100, function(){
				$("#examSec #tabInfoDisp #tabs label#not").trigger( 'click' );
			});
		}
		$("#academicsPage #aboutMenus label").css('background','#F4F4F4');
		$("."+thisClass).css({'background':'rgba(0, 0, 0, 0.1)'});
		$(".aca").fadeOut( 500, function(){
			$("#"+thisClass).fadeIn( 400 );
		});
	});

	$(document).on('click', "#alumni #aluPhotoGallery img", function(){
		$("#photoLightBox img").attr('src', $(this).attr('src'));
		$("#photoLightBox").fadeIn( 500 );
		$("body").css('overflow','hidden');
		thisSrc = $(this).attr('src').split('/');
		window.thisClass = $(this).attr('class');
		window.thisSrc[0];
	});

	$(document).on('click', "#photoLightBox span", function(){
		imageUrl =  $("#photoLightBox img").attr('src');
		splitImgUrl = imageUrl.split('/');
		splitExt = splitImgUrl[splitImgUrl.length - 1].split('.');
		count = 0;
		 imgGalleryCount = $("#alumni #aluPhotoGallery img").each( function(){
			count += 1;
		});
		if( $(this).attr('id') == 'prev' ){
			if( splitExt[0] > 1 ){
				$("#photoLightBox img").attr('src',window.thisSrc[0]+'/'+(Number(splitExt[0]) - 1)+'.jpg');
			}
		}
		else if( $(this).attr('id') == 'next' ){
			if( splitExt[0] < Number(count) ){
				$("#photoLightBox img").attr('src',window.thisSrc[0]+'/'+ (Number(splitExt[0]) + 1) +'.jpg');
			}
		}
	});
