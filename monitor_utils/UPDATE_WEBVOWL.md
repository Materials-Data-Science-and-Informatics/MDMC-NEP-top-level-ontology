# Updating WebVOWL Folder with Exported JSON

If you've exported a JSON file from the WebVOWL website (http://vowl.visualdataweb.org/webvowl.html), you can easily update your webvowl folder with it.

## Quick Method: Using the Script

```bash
# Simplest usage - just specify the module (defaults to ver_3_0)
python monitor_utils/update_webvowl_json.py your-exported-file.json --module core

# For other modules
python monitor_utils/update_webvowl_json.py exported.json --module experiment
python monitor_utils/update_webvowl_json.py exported.json --module dataset
python monitor_utils/update_webvowl_json.py exported.json --module data-analysis-lifecycle
python monitor_utils/update_webvowl_json.py exported.json --module complete

# Explicit path (if needed)
python monitor_utils/update_webvowl_json.py exported.json \
    --webvowl-dir PRIMA/core/ver_3_0/webvowl \
    --ontology-id prima-core
```

## Manual Method

### Step 1: Export JSON from WebVOWL Website

1. Go to http://vowl.visualdataweb.org/webvowl.html
2. Upload your OWL file or paste the IRI
3. Wait for visualization to load
4. Click "Export" → "Export as JSON"
5. Save the JSON file

### Step 2: Place JSON File

Copy the exported JSON file to the correct location (ver_3_0):

```bash
# For core module
cp exported-file.json PRIMA/core/ver_3_0/webvowl/data/prima-core.json

# For experiment module
cp exported-file.json PRIMA/experiment/ver_3_0/webvowl/data/prima-experiment.json

# For dataset module
cp exported-file.json PRIMA/dataset/ver_3_0/webvowl/data/prima-dataset.json

# For data-analysis-lifecycle module
cp exported-file.json PRIMA/data-analysis-lifecycle/ver_3_0/webvowl/data/prima-data-analysis-lifecycle.json

# For complete module
cp exported-file.json PRIMA/complete/ver_3_0/webvowl/data/prima-complete.json
```

**Important**: The filename must match the hash fragment used in the main `index.html`:
- If main `index.html` uses: `webvowl/index.html#prima-core`
- Then JSON file should be: `webvowl/data/prima-core.json`

### Step 3: Verify

Open the main `index.html` in your browser and check that the visualization loads correctly.

## What the Script Does

The `update_webvowl_json.py` script:

1. ✅ Validates the JSON file
2. ✅ Copies it to `webvowl/data/{ontology-id}.json`
3. ✅ Sets up webvowl folder structure if it doesn't exist (copies static files from reference)
4. ✅ Updates the menu in `webvowl/index.html` to include your ontology
5. ✅ Provides helpful feedback and next steps

## Examples

### Example 1: Update ver_3_0 webvowl folder (simplest)

```bash
# You exported prima-core.json from WebVOWL website
# Just specify the module - script handles the rest
python monitor_utils/update_webvowl_json.py ~/Downloads/prima-core.json --module core
```

### Example 2: Update other modules

```bash
# For experiment module
python monitor_utils/update_webvowl_json.py exported.json --module experiment

# For dataset module  
python monitor_utils/update_webvowl_json.py exported.json --module dataset

# For complete module
python monitor_utils/update_webvowl_json.py exported.json --module complete
```

### Example 3: Skip menu update

```bash
# If you only want to update the JSON file
python monitor_utils/update_webvowl_json.py exported.json \
    --module core \
    --no-menu-update
```

## Troubleshooting

### JSON file not found
- Check the file path is correct
- Use absolute path if relative path doesn't work

### WebVOWL folder doesn't exist
- The script will try to create it automatically
- It will copy static files from a reference folder if available
- Or you can specify `--reference-webvowl` to point to an existing webvowl folder

### Menu not updating
- Check that `webvowl/index.html` exists
- The script will warn if it can't find the menu section
- You can manually edit `index.html` if needed

### Visualization not loading
- Verify the JSON filename matches the hash fragment in main `index.html`
- Check browser console for errors
- Ensure JSON file is valid (script validates this)

## Notes

- The static files (CSS, JS, HTML) in webvowl folder are identical across all modules
- Only the JSON file in `data/` folder is module-specific
- You can update the JSON file anytime by running the script again
- The script preserves existing webvowl structure and only updates the JSON file
