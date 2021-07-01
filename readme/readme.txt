Plugin for CudaText.

Provides functionality to search in lines and to extract/filter lines with the
matches. The component was inherited from the dialog "Extract Strings" like in
SynWrite.

Plugin features
---------------

- "Extract Strings..." Dialog

Use this dialog to find by regular expression, substrings in the current editor,
after you found the matches, you have the option to copy them to clipboard or
copy to new tab.

This dialog also has the button "Reg.ex. for e-mail" which sets a common regular
expression to find e-mails.

- "Extract e-mails to new tab" command

Use this command directly to found and all e-mail matches and copy them to a new
tab.

- "Filter lines..." Dialog

Use this dialog to find in current editor tab, all lines containing a simple
string or a regular expression string. This dialog has the next options:

	* Reg.ex - Checkbox to specify that the entered string is a regular
	  expression.
	* Ignore case - Checkbox to set the search to ignore the case for the
	  entered string.
	* Sort output - The new tab with the results will contain the lines sorted.
	* Include line numbers - Add to matches lines a leading string containing
	  the line number with the pattern [##].
	* Keep lexer - The lines with the matches preserves the current editor lexer.
	* Save options - Remember current selected options in the next command
	  execution.
	* Number of lines before match - Simulate the option as "grep -B #" linux
	  command.
	* Number of lines after match - Simulate the option as "grep -A #" linux
	  command.



About
-----

Authors:
  Alexey Torgashin (CudaText)
  @JairoMartinezA (at GitHub)

License: MIT