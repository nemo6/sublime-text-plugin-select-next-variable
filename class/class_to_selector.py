view = None # global

class class_to_selector(sublime_plugin.TextCommand):
	def run(self,edit):
		global view
		view = self.view
		if( len( view.sel() ) == 1 ):
			selection = view.sel()[0]
			m = to_str(selection).split(" ")
			print( m )
			w = ".".join(m)
			content = 'document.querySelectorAll( ".' + w + '" )'
			view.replace( edit, selection , content )

# ...

def to_str(region):
  # view is global
	return view.substr(region)
