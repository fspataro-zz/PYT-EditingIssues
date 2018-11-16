import arcpy
import os
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]
class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False
    def getParameterInfo(self):
        """Define parameter definitions"""
    
        in_features = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
    
        in_applyName = arcpy.Parameter(
            displayName="Apply Name",
            name="in_applyName",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")

        in_name = arcpy.Parameter(
            displayName="Name",
            name="in_name",
            datatype="GPString",
            parameterType="Optional",
            enabled=False,
            direction="Input")
            
        params = [in_features, in_applyName, in_name]
        return params
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True
    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        
        if parameters[1].altered:
            parameters[2].enabled = parameters[1].value
        
        return
    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def execute(self, parameters, messages):
        """The source code of the tool."""
        # parameters
        inFeatures  = parameters[0].valueAsText
        name   = parameters[2].valueAsText
 
        # derived values
        desc = arcpy.Describe(inFeatures)
        workspace = os.path.dirname(desc.path)
        
        messages.addMessage("inFeatures: {0}".format(inFeatures))
        messages.addMessage("Workspace: {0}".format(workspace))
        
        edit = arcpy.da.Editor(workspace)
        messages.addMessage("Editing: {0}".format(edit.isEditing))
        
        edit.startEditing()
        edit.startOperation()
        
        # work
        suffix = ""
        index = 0
        with arcpy.da.UpdateCursor(inFeatures, ["NAME"]) as rows:
            for row in rows:
                row[0] = "{0}{1}".format(name, suffix)
                index += 1
                suffix = " - {0}".format(index)
                rows.updateRow(row)
        
        edit.stopOperation()
        edit.stopEditing(True)
        
        return
