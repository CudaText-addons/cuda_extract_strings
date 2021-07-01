Plugin for CudaText.
Provides functionality to search in lines and to extract/filter lines with the
matches. "Extract strings" functionality was inherited from SynWrite.

Plugin features
---------------

* "Extract Strings..." command

Use this dialog to find, by regular expression, substrings in the current document.
After you found some matches, you have the buttons to copy them to clipboard or copy
to a new tab.

This dialog also has the button "Reg.ex. for e-mail" which sets a common regular
expression to find e-mails.

* "Extract e-mails to new tab" command

Use this command to find and all e-mails in the current document, and copy them
to a new tab. It doesn't show any dialogs, so it's faster to use than
"Extract Strings".

* "Filter lines..." command

Use this dialog to find in the current document all lines containing a simple
string or a regular expression string. Command puts all matched lines to a new tab.
Dialog has the following options:

	* Reg.ex. - Specify that the filter-string is a regular expression.
	* Ignore case - Perform case-insensitive search.
	* Sort output - The new tab with the results will contain the lines sorted.
	* Include line numbers - Add to resulting lines the prefix containing
	  the line number in the form [###] (width depends on maximal line count).
	* Keep lexer - The output tab will have the same lexer as the source tab.
	* Save options - Remember current options in dialog, for the next dialog
	  showing.
	* Number of lines before match - Simulate the option "grep -B #" from Linux.
	* Number of lines after match - Simulate the option "grep -A #" from Linux.


About
-----

Authors:
  Alexey Torgashin (CudaText)
  @JairoMartinezA (at GitHub)
License: MIT
