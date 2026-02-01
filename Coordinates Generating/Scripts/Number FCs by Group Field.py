import arcpy
input_layer = arcpy.GetParameterAsText(0)        # Fc
group_field = arcpy.GetParameterAsText(1)        # Grouping Field
sequence_field = "رقم_النقطة"                     # SeqFieldName

fields = [f.name for f in arcpy.ListFields(input_layer)]
if sequence_field not in fields:
    arcpy.AddField_management(input_layer, sequence_field, "LONG")
else:
    arcpy.AddMessage(f"Field '{sequence_field}' already exists. Skipping creation.")

group_dict = {}
with arcpy.da.UpdateCursor(input_layer, [group_field, sequence_field]) as cursor:
    for row in cursor:
        key = row[0]  
        if key not in group_dict:
            group_dict[key] = 1
        else:
            group_dict[key] += 1
        row[1] = group_dict[key]
        cursor.updateRow(row)
arcpy.AddMessage("Sequence numbers assigned successfully.")
