"""
Web app assets.
"""
from flask_assets import Environment, Bundle

# css = Bundle()
# js_lib = Bundle()
# js_app = Bundle()

def init_app(app):
	"Register static assets."
	webassets = Environment(app)
	# webassets.register('css', css)
	# webassets.register('js_lib', js_lib)
	# webassets.register('js_app', js_app)
	webassets.debug	 = app.debug
	# webassets.cache = not app.debug
	# webassets.manifest = 'cache' if not app.debug esle False
