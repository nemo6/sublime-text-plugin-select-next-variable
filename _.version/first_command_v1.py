import sublime
import sublime_plugin

def remove_element(target_array,list_value):
	for index, value in enumerate(target_array):
		if value in list_value:
			target_array.pop(index)
			# break
	return target_array

def loop_select_word(view):
	for p in view.sel():
		word = view.word(p)
		if word and ( p.begin() == p.end() ) :
			if p.contains(word):
				continue
			a = word.begin()
			b = word.end()
			view.sel().add( sublime.Region( a,b ) )
			view.show( word )

def isAfter( a, b ):
	return a.begin() > b.begin()

# Default (Windows).sublime-keymap
# { "keys": ["ctrl+d"], "command": "select_next_variable" },

class select_next_variable(sublime_plugin.TextCommand):
	def run(self,edit):
		not_a_variable = False
		no_selection = False
		string_scope = False
		view = sublime.active_window().active_view()
		list_variables = view.find_by_selector("variable")
		str_variables = map( lambda x: view.substr(x), view.find_by_selector("variable") ) # list_variables muted by "remove_element"
		first_selection = view.sel()[-1]
		current_selection = { "text": view.substr(first_selection) }
		slice_selection = remove_element( list_variables , view.sel() )
		scope = view.scope_name( first_selection.begin() )

		loop_select_word(view)

		# h = list(map( lambda x : { "text": view.substr(x), "position":x } , slice_selection ))
		# h = list(filter( lambda x: x["text"] == current_selection["text"], h ))
		# if( len(h) != 0 ):
		# 	h.pop(0)
		# print( current_selection["text"], first_selection )
		# print( *h,sep="\n" )

		if( len( view.sel() ) > 1 ):
			# print("multi-selection")
			if "string" in view.scope_name( view.sel()[0].begin() ):
				# print("in a string scope")
				not_a_variable = True

		if( ( first_selection.begin() == first_selection.end() ) and len(view.sel()) == 1 ):
			no_selection = True

		if not current_selection["text"] in str_variables :
			not_a_variable = True

		if "string" in scope:
			not_a_variable = True

		if not_a_variable :
			# print( "Not a variable" )
			next_position = view.find( current_selection["text"], first_selection.end() )
			if next_position.begin() == -1:
				return
			# if next_position in list_variables:
			# 	return
			a = next_position.begin()
			b = next_position.end()
			view.sel().add( sublime.Region( a,b ) )
			view.show( first_selection )
			return

		# print( *list(filter( lambda x: x == current_selection["text"], str_variables )) )
		# print( "Is a variable" )
		# print( *str_variables )
		# print( *slice_selection )

		for object_position in slice_selection:
			text = view.substr(object_position)
			if ( current_selection["text"] == text and isAfter( object_position , first_selection ) ):
				a = object_position.begin()
				b = object_position.end()
				view.sel().add( sublime.Region( a,b ) )
				view.show( object_position )
				break

# { "keys": ["è"], "command": "add_backtick" },

class add_backtick(sublime_plugin.TextCommand):
	def run(self,edit):
		view = sublime.active_window().active_view()
		first_selection = view.sel()[0]
		a = first_selection.begin()
		b = first_selection.end()
		self.view.insert( edit, a , "`" )
		self.view.insert( edit, b+1 , "`" )

class add_cursor_comma(sublime_plugin.TextCommand):
	def run(self,edit):
		view = sublime.active_window().active_view()
		print( *view.sel() )
		cursor_selection = view.sel()[-1]
		cursor_pos = view.sel()[0].begin()
		a = view.sel()[0].begin()
		b = view.sel()[0].end()
		next_char = view.substr( sublime.Region( cursor_pos , cursor_pos + 1 ) )
		after_comma = { "region": sublime.Region( a + 1 , b + 2 ) , "word": view.word( sublime.Region( a + 1 , b + 2 ) )}
		print( "next_char", next_char )
		print( "after_comma", *list( map( lambda x : ord(x) , view.substr(after_comma["word"]) ) ) )

		if( len(next_char) != 0 and next_char == "," ):
			word = view.word(cursor_pos)
			word_text = view.substr(word)[:-1]
			if( word_text.isspace() ):
				return
			if word:
				a = word.begin()
				b = word.end()
				view.sel().add( sublime.Region( a,b ) )
				view.show( word )
			if( view.substr(after_comma["word"])[0] != "," ):
				a = after_comma["word"].begin()
				b = after_comma["word"].end()
				view.sel().add( sublime.Region( a,b ) )
				view.show( word )

			new_cursor_pos = cursor_pos + 1
			view.sel().add(sublime.Region(new_cursor_pos))
		else:
			print(None)

"""

# def get_command_name(caption):
# 	commands = sublime.load_resource("Packages/User/Default.sublime-commands")
# 	commands = sublime.decode_value(commands)
# 	return commands
# 	for command in commands:
# 		if command["caption"] == caption:
# 			return command["command"]
# 	return None

# class HelloWorldCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		caption = "[RegReplace] Format : Space arround parenthesis and brackets"
# 		command_name = get_command_name(caption)
# 		if command_name:
# 			sublime.active_window().run_command( command_name[0]["command"] , command_name[0]["args"] )
# 			self.view.insert( edit, self.view.sel()[0].begin(), "hello world" )

"""

# class HelloWorldCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		self.view.insert(edit, self.view.sel()[0].begin(), "hello world")
