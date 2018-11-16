Crazy technical issue... I'm creating a set of "helper tools" for power editors in an enterprise environment.  Ideally the tools will run correctly when the user is "in an arcmap edit session" or not.  I'd be fine with forcing them users to only be in an edit session when using the tools but the problem there is that after edits are made by the tool.  The arcmap editor doesn't seem to know changes have been made; clicking the "stop editing" button doesn't present the user with the save option and dumps the edits.  This is probably an edge case but --- man --- will users be mad if they lose edits and the proper attribution doesn't get pushed during a reconcile/post. Details:

[GeoNet discussion](https://community.esri.com/message/813870-is-it-possible-for-a-pyt-tool-to-notify-the-arcmap-edit-session-that-edits-have-been-made)

### SETUP

* SQLServer database
	* geodatabase enabled

* Feature dataset
		* Feature class
    * GlobalIds added
    * Editor tracking enabled
    * registered as versioned
    * Archiving Enabled

* Python toolbox (pyt)
	* based on template/help sample
		* opens arcpy.da.UpdateCursor
			* sets text field to input value
			* updateRow()

* Geoprocessing Options
	* Background Processing disabled
	* Note: I re-ran all the test below with "background process enabled" but it doesn't appear to use the background processor for pyt tools. (?)

### TEST SCENARIO/RESULTS

* If 'ArcMap edit session' is closed, tools fails as expected:
	* "Objects in this class cannot be updated outside an edit session [TestsGDB.DBO.TES_Polygon]"


* If 'arcmap edit session' is open, tool succeeds, attribute update is visible in table.
  * __However, when clicking "stop editing", there's no warning that edits are pending and the session will close and reset the data.__

* Added arcpy.da.Editor to check if 'isEditing':
returns false regardless of the ArcMap editor state --- makes sense that it's not the same session

![](/editing-false-expected.png)

![](/editing-false-not-helpful.png)

* Added editor.startOperation() and editor.stopOperation() with the ArcMap edit session open
	* fails with "start an edit session"

![](/start-operation.png)

* Added editor.startEditing() with the ArcMap edit session open, but no closing editor.stopEditing()
	* this produces a successful tool run and the "save		* edits" dialog prompts when clicking 'stop editing'
  * when the ArcMap edit session is closed, the tool will appear to run successfully but the edits don't persist. This seems logical since I never closed the session.

![](/start-editing.png)

* Adding editor.stopEditing() with the arcmap session open
	* this throws an error on the editor.stopEditing() with the message - "start edit session"
	* this result baffles me ????
	* the attribute edits are correctly placed and the "save edits" dialog prompts when clicking 'stop editing'. So it's almost correct behavior except for the "tool failed result"
	* when the ArcMap edit session is closed, the tool will execute as expected and the edits persist

![](/stop-editing.png)

It seems like my choice is use the full script edit session management and sink the error on stopEditing so it works in and out of the ArcMap edit session or don't use the script edit session and the user can only work in an ArcMap session and might not get the prompt.