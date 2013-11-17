(function ($) {
	$.Mustache.load('templates.html')
		.done(function() {
			routie({
				'/etusivu': function() {
					$('section').mustache('etusivu', null, { method: 'html' });
				},
				'/rajoitteet': function() {
					$.getJSON('rajoite', function(data) {
						$('section').mustache('rajoitteet', data, { method: 'html' });
					});
				},
				'/rajoite/:id': function(id) {
					$.getJSON('rajoite/' + id, function(data) {
						$('section').mustache('rajoite', data, { method: 'html' });
					});
				},
				'/kirjaudu': function() {
					$('section').mustache('kirjaudu', null, { method: 'html' });
				},
				'/rajoita': function() {
					$('section').mustache('teerajoite', null, { method: 'html' });
				},
				'*': function() {
					routie('/etusivu');
				}
			});
		});
})(jQuery);
