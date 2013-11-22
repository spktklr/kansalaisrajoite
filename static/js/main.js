(function ($) {
	var convertToSlug = function(text, render) {
		return render(text)
		.toLowerCase()
		.replace(/[^\w ]+/g, '')
		.replace(/ +/g, '-');
	}
	
	var convertToDateStr = function(text, render) {
		var timestamp = parseInt(render(text))*1000;
		return new Date(timestamp).toLocaleDateString();
	}
	
	var percentCompleted = function(text, render) {
		var threshold = 5;
		return ((Math.min(parseInt(render(text)), threshold) / threshold) * 100);
	}
	
	var show = function(element, template, data) {
		$(element).mustache(template, (data === undefined ? null : data), { method: 'html' });
	}
	
	$.Mustache.load('templates.html')
		.done(function() {
			routie({
				'': function() {
					// default to the front page
					show('section', 'etusivu');
				},
				'/etusivu': function() {
					show('section', 'etusivu');
				},
				'/rajoitteet': function() {
					$.getJSON('rajoite', function(data) {
						data.slug = function() { return convertToSlug; };
						data.date = function() { return convertToDateStr; };
						data.percentCompleted = function() { return percentCompleted; };
						show('section', 'rajoitteet', data);
					});
				},
				'/rajoite/:id/*': function(id) {
					$.getJSON('rajoite/' + id, function(data) {
						data.date = function() { return convertToDateStr; };
						show('section', 'rajoite', data);
					});
				},
				'/kirjaudu': function() {
					show('section', 'kirjaudu');
				},
				'/rajoita': function() {
					show('section', 'teerajoite');
				},
				'/tiedotteet': function() {
					$.getJSON('tiedote', function(data) {
						data.hasNews = (data.news.length > 0);
						data.date = function() { return convertToDateStr; };
						show('section', 'tiedotteet', data);
					});
				},
				'/pasvenska': function() {
					show('section', 'pasvenska');
				},
				'/inenglish': function() {
					show('section', 'inenglish');
				},
				'*': function() {
					// show 404 page for other urls
					show('section', '404');
				}
			});
			
			// catch all ajax errors and show error page
			$(document).ajaxError(function(event, request, settings) {
				if (request.status === 401) {
					show('section', 'kirjaudu');
				} else {
					show('section', 'virhe');
				}
			});
		});
})(jQuery);
