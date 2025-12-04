import json
import re

# Function to recursively modify OPC tags

# CONFIG (1/2)

def modify_opc_tags(tags, parameter_name='genNumber'):
    if not isinstance(tags, list):
        return 0

    mod_count = 0
    for tag in tags:
        if (
            tag.get('tagType') == 'AtomicTag' and
            tag.get('valueSource') == 'opc' and
            isinstance(tag.get('opcItemPath'), str)
        ):
            original_path = tag['opcItemPath']
            modified_binding = original_path.replace('emcp2', 'emcp{' + parameter_name + '}')

            tag['opcItemPath'] = {
                'bindType': 'parameter',
                'binding': modified_binding
            }
            mod_count += 1
            print('Updated OPC path for tag "%s"' % tag.get('name', 'unknown'))

        # Recurse into nested tags
        if 'tags' in tag:
            mod_count += modify_opc_tags(tag['tags'], parameter_name)

    return mod_count

# Function to add/modify the BasePath parameter in the root JSON
def ensure_basepath_parameter(json_data):
    if 'parameters' not in json_data:
        json_data['parameters'] = {}

    if 'BasePath' not in json_data['parameters']:
        json_data['parameters']['BasePath'] = {
            'dataType': 'String',
            'value': ''
        }
        print('Added new parameter: "BasePath"')
    else:
        print('BasePath parameter already exists; skipping addition.')

# Function to recursively modify expression tags using BasePath + concat
def modify_expression_tags(tags):
    if not isinstance(tags, list):
        return 0

    mod_count = 0
    # Pattern to match the full tag reference (e.g., "{[ST_POWER]...sanchez_emcp2_modbus/<suffix>}")
    tag_ref_pattern = r'\{(\[ST_POWER\]Microgrid/Gen Garden/Data Tags/sanchez_emcp2_modbus/[^}]+)\}'

    for tag in tags:
        if (
            tag.get('tagType') == 'AtomicTag' and
            tag.get('valueSource') == 'expr' and
            'expression' in tag and
            isinstance(tag.get('expression'), str) and
            re.search(tag_ref_pattern, tag['expression'])
        ):
            full_expression = tag['expression']
            # Find all matches in the expression (handles multiple per expression)
            matches = list(re.finditer(tag_ref_pattern, full_expression))
            if matches:
                # Build new expression by replacing each match
                new_expression_parts = []
                last_end = 0
                for match in matches:
                    # Add the part before this match
                    new_expression_parts.append(full_expression[last_end:match.start()])
                    # Extract suffix after "sanchez_emcp2_modbus/" (e.g., "Generator_Phase_B_Apparent_Power/status/stVal")
                    inner_part = match.group(1)
                    suffix = inner_part.replace('', '')
                    # Replace with tag() function: "tag({BasePath} + '/suffix')"  # Updated to use tag() for proper dereferencing
                    new_expression_parts.append("tag({BasePath} + '/" + suffix + "')")
                    last_end = match.end()
                # Add the remaining part after the last match
                new_expression_parts.append(full_expression[last_end:])
                # Join all parts
                tag['expression'] = ''.join(new_expression_parts)

                mod_count += 1
                print('Modified expression for tag "%s":\n  Old: %s\n  New: %s\n' % (tag['name'], full_expression, tag['expression']))
            else:
                print('Warning: Expression for "%s" matched pattern but couldn\'t extract suffix: %s' % (tag['name'], full_expression))

        # Recurse into nested tags
        if 'tags' in tag:
            mod_count += modify_expression_tags(tag['tags'])

    return mod_count

# Main function
def main():
    # CONFIG (2/2)
    file_path = 'json.json'  # replace with name of JSON file

    try:
        # Read and parse the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Add/update BasePath parameter
        ensure_basepath_parameter(data)

        # Modify OPC tags (uncomment if needed; it's safe to run—it skips already converted ones)
        opc_mods = 0
        if 'tags' in data:
            opc_mods = modify_opc_tags(data['tags'])

        # Modify expression tags
        expr_mods = 0
        if 'tags' in data:
            expr_mods = modify_expression_tags(data['tags'])

        # Write the modified JSON back to the file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)  # Pretty-print with indent=2
        print('\nModification complete!\n- BasePath parameter: Added/updated\n- OPC changes: %d\n- Expression changes: %d\nFile updated: %s' % (opc_mods, expr_mods, file_path))
    except Exception as e:
        print('Error processing the file: %s' % e)
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
