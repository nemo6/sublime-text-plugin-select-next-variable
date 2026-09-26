# select_next_variable, CTRL + D
import sublime
import sublime_plugin
import re

cursor_in_console = False
view = None

# in : select_next_variable
# def isBefore( a, b ):
# 	return a.begin() < b.begin()

# in : select_next_variable
def isAfter( a, b ):
	return a.begin() > b.begin()

# in : select_next_variable
def remove_element(target_array,list_value):
	for index, value in enumerate(target_array):
		if value in list_value:
			target_array.pop(index)
	return target_array

# in : select_next_variable
def loop_select_word( view ):
	max = len( view.sel() )
	counter = []
	for p in view.sel():
		word = view.word(p)
		# print( view.substr( word ) )
		if word and ( p.begin() == p.end() ) :
			if p.contains(word):
				continue
			a = word.begin()
			b = word.end()
			view.sel().add( sublime.Region( a,b ) )
			view.show( word )
			counter.append(1)

	if( sum( counter) == max ):
		return True
	else:
		return False

def count_instance( m , value ):
	count = 0
	for x in m:
		if x == value :
			count += 1
	return count

# filter_by_region
def filter_by_region3( m1 , m2 ):
	m = []
	for x in m1:
		if x not in m2:
			m.append( x )
	return m

# in : select_next_variable, update_variable_selection
def find_variable(view):
	selectors = [
		"variable",
		"support.module.node.js",
		"source.js.embedded.expression",
		"support.type.object.node.js",
		# "entity.name.function.js",
		# "storage.type.js",
	]
	acc=[]
	for selector in selectors:
		acc.extend( view.find_by_selector(selector) )

	acc.sort( key=lambda x : x.begin() )

	return acc

# in : select_next_variable
def scope_name( view,region ):
	return view.scope_name( region.begin() ).strip().split(" ") # [-1]
	# return view.extract_scope( x )

def line_to_range_region( region ):
	line_range = list( range( region.begin() , region.end() ) )
	return list( map( lambda x : sublime.Region(x,x+1) , line_range ) )

def f_split( sr ):
	return list( map( lambda x : sublime.Region( x , x+1 ) , sr ) )

def f_split_region_to_range( sublime_region ):
	a = sublime_region.begin()
	b = sublime_region.end()
	w = []
	for x in range( a , b + 1 ):
		w.append( sublime.Region( x,x+1 ) )
	return w

#

def find_function_call(self):

	update_regions = self.view.find_by_selector( "meta.function-call.js" )
	# variable.function.js

	# for [i,region] in enumerate(regions):
	# 	if "storage.type.function.js" in scope_name( self.view, region ):
	# 		update_regions.append( region )

	level_block = 0

	list_results = []
	for region in update_regions:
		# print( [view.substr( region ).strip()] )
		# m = list( filter( lambda x : x[-1] in [46,89] , m ) )
		f = list( filter( lambda x : x == "meta.block.js" , scope_name( view , region ) ) )
		level_block = len(f)
		v = detect_scope_argument2( f_split_region_to_range(region) , level_block )
		list_results.append( v )

	return list_results

def detect_scope_argument2( array , level_block ):
	# print( array )
	function_name = ""
	region = []
	is_var_detected = False
	variables_names = [ "" ]

	for x in array:
		v = scope_name( view , x )[-1]
		# print( v )
		if re.search( "variable.function.js" , v ):
			function_name += view.substr(x)
			region.append( x.begin() )
			continue
		if re.search( "variable." , v ):
			is_var_detected = True
			variables_names[-1] += view.substr(x)
		else:
			if is_var_detected:
				variables_names.append( "" )
				is_var_detected = False

	# filter variables_names from empty value
	return [ level_block , function_name , variables_names[:-1] ] # [region[0],region[-1]]

#

def find_argument_function(self):

	regions = self.view.find_by_selector( "meta.function.declaration.js" )
	update_regions = []

	for [i,region] in enumerate(regions):
		if "storage.type.function.js" in scope_name( self.view, region ):
			update_regions.append( region )

	list_results = []
	for region in update_regions:
		f = list( filter( lambda x : x == "meta.block.js" , scope_name( view , region ) ) )
		level_block = len(f)
		v = detect_scope_argument( f_split_region_to_range(region) , level_block )
		list_results.append( v )

	return list_results

def detect_scope_argument( array, level_block ):
	# print( array )
	function_name = ""
	variables_names = [ "" ]
	is_var_detected = False

	for x in array:
		v = scope_name( view , x )[-1]
		# print( v )

		if re.search("entity.name.function.js" , v ):
			function_name += view.substr(x)
			continue

		# if re.search( "variable.parameter" , v ):
			# TO DO : work only for variable with one character
			# variables_names.append( [ view.substr(x) , x ] )

		if re.search( "variable.parameter" , v ):
			is_var_detected = True
			variables_names[-1] += view.substr(x)
		else:
			if is_var_detected:
				variables_names.append( "" )
				is_var_detected = False

	# filter variables_names from empty value
	return [ level_block, function_name , variables_names[:-1] ] # [region[0],region[-1]]
	# return { "function_name":function_name , "variables_names":variables_names[:-1] } # [ variables_names]

# SCOPE START : select_next_variable

highlight_array = []

class select_next_variable( sublime_plugin.TextCommand ):
	def run(self,edit):
		global view
		view = self.view

		if( len( highlight_array ) != 0 ):
			for key in [ "group_punct" ]:
				self.view.erase_regions(key)
			del highlight_array[:]
			return

		first_selection = self.view.sel()[-1]

		# target_variable = "volt"
		# detect current meta block ( meta.block.js ) before searching match for variable name

		print( find_function_call(self) )
		print( find_argument_function( self ) )

		# highlight_array.append( update_regions )
		# self.view.add_regions( "group_punct", update_regions, scope="comment", flags=sublime.DRAW_NO_FILL)
		# return
		# for region in regions:
		# 	print( scope_name( self.view , region ) )

		# print( first_selection )
		# print( scope_name( self.view , first_selection.begin() ) )
		# print( view.find_by_selector( "meta.group.js" ) )
		# print( view.extract_tokens_with_scopes( sublime.Region( 0 , self.view.size() ) ) )

class select_next_variable2( sublime_plugin.TextCommand ):

	def run(self,edit):

		not_a_variable = False

		selectors = [
			"variable",
			"support.module.node.js",
			"source.js.embedded.expression",
			"support.type.object.node.js",
			# "variable.other",
			# "variable.other.object.js",
			# "entity.name.function.js",
			# "storage.type.js",
		]

		# fulltext = self.view.substr( sublime.Region( 0 , self.view.size() ) )

		view = self.view

		list_variables = find_variable(view)

		str_variables = list( map( lambda x : view.substr(x), list_variables ) )

		first_selection = view.sel()[-1]

		type_scope = scope_name( first_selection.begin() )

		re_value = re.compile( selectors[0] )

		if  not re.search( r"variable|variable\.|meta\.generic-name\.|entity\.name\.function\.js|support\.module\.node\.js|source\.js\.embedded\.expression|support\.type\.object\.node\.js" , type_scope ) :
			not_a_variable = True

		# select the current variable/word
		bool_loop_select_word = loop_select_word( view )

		slice_selection = remove_element( list_variables , view.sel() )

		scope = view.scope_name( first_selection.begin() )

		current_selection = view.substr( view.sel()[-1] )

		n = count_instance( str_variables, current_selection )

		if( n < 2 ):
			not_a_variable = True

		if( len( view.sel() ) >= 1 ):
			if "string" in view.scope_name( view.sel()[0].begin() ):
				# print( "in a string scope" )
				not_a_variable = True
				return

		if( ( first_selection.begin() == first_selection.end() ) and len( view.sel() ) == 1 ):
			bool_loop_select_word = True

		if not current_selection in str_variables :
			not_a_variable = True

		if "string" in scope:
			not_a_variable = True

		if not_a_variable :

			if( bool_loop_select_word ) :
				return

			selection = view.sel()[-1]
			current_selection = view.substr( selection )
			list_words = view.find_all( current_selection, selection.end() )
			update_list_words = filter_by_region3( list_words, list_variables )

			for x in update_list_words:
				if isAfter( x , selection ) :
					a = x.begin()
					b = x.end()
					view.sel().add( sublime.Region( a,b ) )
					view.show( sublime.Region( a,b ) )
					break
			return

		for object_position in slice_selection:
			text = view.substr(object_position)
			if  view.substr(first_selection) == text and isAfter( object_position , first_selection ) :
				a = object_position.begin()
				b = object_position.end()
				view.sel().add( sublime.Region( a,b ) )
				break

# SCOPE END : select_next_variable

class is_console_open( sublime_plugin.WindowCommand ):
	def run(self):
		global cursor_in_console
		view = self.window.active_view()
		panel = self.window.active_panel()
		is_console_open = (panel == "console")
		# print( "is_console_open" , is_console_open )
		# print( "cursor_in_console", cursor_in_console )
		if not is_console_open:
			# print( "open console for the first time" )
			self.window.run_command( "show_panel" , { "panel": "console" } )
			cursor_in_console = True
			return

		active_view = self.window.active_view()
		console_view = self.window.find_output_panel("console")
		if cursor_in_console:
			# print("focus_group")
			self.window.run_command( "focus_group", { "group": 0 } )
			cursor_in_console = False
		else:
			# print("focus console")
			self.window.run_command( "show_panel", { "panel": "console" } )
			cursor_in_console = True
